"""
Napalm driver for ArubaOS 505 Wi-Fi Device using SSH.
Read https://napalm.readthedocs.io for more information.
"""

from napalm.base import NetworkDriver
from napalm.base.exceptions import (
    ConnectionException,
    SessionLockedException,
    MergeConfigException,
    ReplaceConfigException,
    CommandErrorException,
    )


import paramiko
from files_helpers import FileHandler
import time


def ssh_connector(hostname, username, password, key=False, timeout=10, port=22):
    """ Connect to remote device and return a channel to use for sending cmds.
        return the returned value is the channel object that will be used to send command to remote device
    """
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, port=port, username=username,
                    password=password, look_for_keys=key, timeout=timeout)

    except:
        print("Could not connect to {0}".format(hostname))
        #ssh.close()
        #return None
    else:
        print("Connected to {0}\n".format(hostname))
        channel = ssh.invoke_shell()
        return channel


def send_single_cmd(cmd, channel, incoming_sleep_time=4, out_going_sleep_time=4):
    """Send cmd via the channel if channel object is not None
        return: the return value is the result or the executed cmd
    """
    if not cmd:
        print(f"Not command to send\n")
        return None
    if not channel:
        print(f"No channel available\n")
        return None

    banner = channel.recv(99999).decode("utf-8")
    time.sleep(1)
    print(f"{banner}\n\n")
    time.sleep(1)

    channel.send(cmd + "\n")
    time.sleep(out_going_sleep_time)

    output = channel.recv(99999).decode("utf-8")
    time.sleep(incoming_sleep_time)
    return output


class ArubaOS505(NetworkDriver):
    """Napalm driver for ArubaOS 505 Wi-Fi Device."""

    def __init__(self, hostname, username, password, timeout=60, optional_args=None):
        """Initializer."""

        self.hostname = hostname
        self.username = username
        self.password = password
        self.timeout = timeout

        self.session_info = None
        self.isAlive = False
        if not optional_args:
            optional_args = {}

        self.file_handler = FileHandler()



    def open(self):
        """
        Implementation of NAPALM method 'open' to open a connection to the device.
        """
        try:
            self.session_info = ssh_connector(hostname=self.hostname,username=self.username,
                                              password=self.password)
            self.isAlive = True
            print(f"connected to ---  {self.hostname}\n\n")
        except ConnectionError as error:
            # Raised if device not available
            #raise ConnectionException(str(error))
            print(f"Failed to connect to {self.hostname}\n\n")


    def close(self):
        """
        Implementation of NAPALM method 'close'. Closes the connection to the device and does
        the necessary cleanup.
        """
        self.isAlive = False
        self.session_info.close()


    def is_alive(self):
        """
        Implementation of NAPALM method 'is_alive'. This is used to determine if there is a
        pre-existing connection that must be closed.
        :return: Returns a flag with the state of the connection.
        """
        return {"is_alive": self.isAlive}

    def get_config(self, retrieve="all", full=False, sanitized=False):
        """
        :return: The object returned is a dictionary with a key for each configuration store:
            - running(string) - Representation of the  running configuration
        """

        configs = {
            "running": "",
            "startup": "No Startup",
            "candidate": "No Candidate"
        }

        if retrieve.lower() in ('running', 'all'):
            command = "show running-config"
            try:
                channel = ssh_connector(self.hostname, self.username, self.password)
            except Exception as e:
                print(f"Failed to interact with: {self.hostname} \n")
                print(e)
            else:
                self.isAlive = True
                output = send_single_cmd(command, channel)
                configs['running'] = output

                data = str(configs['running']).split("\n")
                non_empty_lines = [line for line in data if line.strip() != ""]

                string_without_empty_lines = ""
                for line in non_empty_lines:
                    string_without_empty_lines += line + "\n"
                configs['running'] = string_without_empty_lines
                channel.close()
                self.close()
        if retrieve.lower() in ('startup', 'all'):
            ...

        return configs

    def get_facts(self):
        """Return a set of facts from the devices."""

        configs = {}
        show_summary = "show summary"
        show_version = "show version"

        try:
            channel = ssh_connector(self.hostname, self.username, self.password)
        except:
            print(f"Failed to interact with: {self.hostname} \n")
        else:
            summary_output = send_single_cmd(show_summary, channel)
            configs['running_'] = summary_output

            data = str(configs['running_']).split("\n")
            non_empty_lines = [line for line in data if line.strip() != ""]

            string_without_empty_lines = ""
            for line in non_empty_lines:
                string_without_empty_lines += line + "\n"
            hostname_, fqdn_, serial_number_ = self.file_handler.show_summary_sanitizer(string_without_empty_lines)

            try:
                channel2 = ssh_connector(self.hostname, self.username, self.password)
            except:
                print(f"Failed to interact with: {self.hostname} \n")
            else:
                # Show version data processing here
                show_version_output = send_single_cmd(show_version, channel2)
                configs['show_version'] = show_version_output
                show_version_data = str(configs['show_version']).split("\n")

                show_version_non_empty_lines = [line for line in show_version_data if line.strip() != ""]
                show_version_string_without_empty_lines = ""
                for line in show_version_non_empty_lines:
                    show_version_string_without_empty_lines += line + "\n"

                vendor, model, os_version, uptime = self.file_handler.show_version_sanitizer(
                    show_version_string_without_empty_lines)

                if channel:
                  channel.close()
                if channel2:
                    channel2.close()

                self.close()

                return {
                        "hostname": str(hostname_),
                        "fqdn": fqdn_,
                        "vendor": str(vendor),
                        "model": str(model),
                        "serial_number": str(serial_number_),
                        "os_version": str(os_version),
                        "uptime": uptime,
                    }

    def get_environment(self):
        environment = {}
        environment.setdefault("cpu", {})
        environment["cpu"][0] = {}

        environment.setdefault("memory", {})
        environment["memory"]["used_ram"] = "dummy data"



        # Initialize 'power' and 'fan' to default values (not implemented)
        environment.setdefault("power", {})
        environment["power"]["invalid"] = {
            "status": True,
            "output": -1.0,
            "capacity": -1.0,
        }
        environment.setdefault("fans", {})
        environment["fans"]["invalid"] = {"status": True}

        return environment



