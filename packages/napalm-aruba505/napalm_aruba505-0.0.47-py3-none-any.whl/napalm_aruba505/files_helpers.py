# Easier to store these as constants
SECONDS = 1
MINUTE_SECONDS = 60
HOUR_SECONDS = 3600
DAY_SECONDS = 24 * HOUR_SECONDS
WEEK_SECONDS = 7 * DAY_SECONDS
YEAR_SECONDS = 365 * DAY_SECONDS


class FileHandler:

    def __init__(self):
        pass

    def show_version_sanitizer(self, data):
        """ Collects the vendor, model, os version and uptime from the 'show version'
        :returns a tuple with two values (vendor, model, os version, uptime)
        """

        # Initialize the vars to zero
        (years, weeks, days, hours, minutes, seconds) = (0, 0, 0, 0, 0, 0)

        vendor = "Hewlett Packard"
        model = ""
        os_version = ""
        uptime = ""

        if data:
            data_l = data.strip().splitlines()
            for l in data_l:
                if "MODEL" in l:
                    temp_data = l.replace("(", "").replace(")", "")
                    temp_model, temp_version = temp_data.split(",")
                    if "MODEL:" in temp_model:
                        t = str(temp_model).split()[-1]
                        if t:
                            model = t
                    if "Version" in temp_version:
                        v = str(temp_version).split()[-1]
                        if v:
                            os_version = v
                if "AP uptime is" in l:
                    tmp_uptime = l.replace("AP uptime is", "").split()
                    uptimes_records = [int(i) for i in tmp_uptime if i.isnumeric()]

                    if uptimes_records:
                        weeks, days, hours, minutes, seconds = uptimes_records
                        uptime = sum([
                            (years * YEAR_SECONDS),
                            (weeks * WEEK_SECONDS),
                            (days * DAY_SECONDS),
                            (hours * HOUR_SECONDS),
                            (minutes * MINUTE_SECONDS),
                            (seconds * SECONDS), ])
        return vendor, model, os_version, uptime


    def show_summary_sanitizer(self, data):
        """ Collects the fqdn and the serial number from the 'show summary'
        :returns a tuple with two values (hostname, fqdn, serial_number)
        """

        fqdn = ""
        serial_number = ""
        hostname_ = ""

        if data:
            data_l = data.strip().splitlines()

            for l in data_l:
                if "Name" in l and not hostname_:
                    hostname_ = f"{l.split(':')[1].lower()}"
                if "DNSDomain" in l and hostname_:
                    fqdn = f"{hostname_}.{l.split(':')[1]}"
                if "Serial Number" in l :
                    serial_number = l.split(':')[1]
        return hostname_, fqdn, serial_number























