import intelpy.config
from pathlib import Path
from sys import platform
from os import makedirs
from datetime import datetime

class logger(intelpy.config.Config):

    def __init__(self, app_name, logfile="debug.log", debug=0):
        self.app_name = app_name
        self.default_log_file = logfile
        self.default_config_file = logfile
        self.file_location = self.good_place_for_file()
        self.debug = debug

        # If debug.log doesn't exist, create it and set default values
        if not Path(self.file_location + self.default_log_file).is_file():
            # Create directory as well if it doesn't exist
            if not Path(self.file_location).exists():
                try:
                    if self.debug:
                        print("Making " + str(self.file_location))
                    makedirs(self.file_location)
                except IOError as e:
                    if self.debug:
                        print("Could not access directory path for debug log, check permissions")
                    print(str(e))
                    raise

            self.flush_config_to_file("== Logging instance started ==")

    def read_config_from_file(self):
        pass

    def flush_config_to_file(self, log_to_append):
        #if self.debug:
        #    print("Writing log to: " + str(self.file_location + self.default_log_file))
        try:
            with open(self.file_location + self.default_log_file, "a", encoding="utf-8") as log_file:
                now = datetime.now()
                date_time_stamp = now.strftime("%m/%d/%Y %H:%M:%S")
                log_file.write("[" + str(date_time_stamp) + "] " + str(log_to_append) + "\n")
        except IOError as e:
            if self.debug:
                print("Could not write to log file")
            print(str(e))
            raise

    def write_log(self, log_to_append):
        self.flush_config_to_file(log_to_append)
        print(log_to_append)

    def debug_config(self, configuration):
        # takes the JSON from IntelPy and prints out the values
        self.write_log("** Debug Configuration Values **")
        self.write_log("Home system: " + configuration.value["home_system"])
        self.write_log("Eve Log Location: " + configuration.value["eve_log_location"])
        self.write_log("All watched channels:")
        for channel in configuration.value["watched_channels"]:
            self.write_log("- " + channel)

        self.write_log("Alert systems:")
        self.write_log(configuration.value["alert_systems"])
        self.write_log("Alert jumps: " + str(configuration.value["alert_jumps"]))

        self.write_log("Watch active? " + str(configuration.value["log_watch_active"]))
        self.write_log("Config loc: " + configuration.value["config_loc"])
        self.write_log("Alarm sound: " + configuration.value["alarm_sound"])
        self.write_log("Display alerts? " + str(configuration.value["display_alerts"]))
        self.write_log("Display clear? " + str(configuration.value["display_clear"]))
        self.write_log("Display all? " + str(configuration.value["display_all"]))

        self.write_log("** END Debug Configuration Values **")