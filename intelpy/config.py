import json
import os
from sys import platform


class Config:
    """
    Config class - Load and save configuration values in a neat little object.

    Serializes configuration to/from JSON to/from disk and supports Linux, FreeBSD, OSX and Windows.
    Saves a default configuration (specified) if none exists.
    Uses ~/.config/appname/ or c:/home/users/AppData/Local/appname/ to save the configuration under.

    Usage:

        obj = config.Config(name_of_ application, default_JSON, (optional) file_name)

        where:
            name_of_application = the shorthand name of the app
            default_JSON = JSON formatted object to set as the default config if none exists
            (optional) file_name = name of the file to save the config, e.g. settings.json

    Methods:

        obj.read_config_from_file()  - read in configuration file from disk
        obj.flush_config_to_file()   - flush the current configuration values to disk
        obj.good_place_for_file()    - returns the best place to save the file depending on OS. Used internally.

    Accessing values:0

        print(obj.value["Key"])               - prints the value in Key
        print(obj.value["my_list"][0])        - prints the first value in a list called my_list
        for value in obj.value["my_list"]:    - iterates over the list
            print(value)
    """

    def __init__(self, app_name, default_config_json, default_config_file="settings.json"):
        self.value = default_config_json                 # Config values stored in here
        self.default_config_file = default_config_file   # os.path to file (without filename)
        self.app_name = app_name                         # App name for the folder to save in
        self.file_location = self.good_place_for_file()  # os.path excluding filename to save/read file
        self.debug = 0

        # If settings.json doesn't exist, create it and set default values
        if not os.path.exists(self.file_location + self.default_config_file):
            # Create directory as well if it doesn't exist
            if not os.path.exists(self.file_location):
                try:
                    if self.debug:
                        print("Making " + str(self.file_location))
                    os.makedirs(self.file_location)
                except IOError as e:
                    if self.debug:
                        print("Could not access directory path for config, check permissions")
                    print(str(e))
                    raise

            self.flush_config_to_file()

        # settings.json should hopefully exist now, read it in
        self.read_config_from_file()

    def read_config_from_file(self):
        # LOAD (deserialize) JSON file into an object
        if self.debug:
            print("Reading config from: " + str(self.file_location + self.default_config_file))
        try:
            with open(self.file_location + self.default_config_file, "r") as config_file:
                self.value = json.load(config_file)
        except IOError as e:
            if self.debug:
                print("Could not read configuration file")
            print(str(e))
            raise

    def flush_config_to_file(self):
        # DUMP (serialize) an object to JSON file
        if self.debug:
            print("Writing config to: " + str(self.file_location + self.default_config_file))
        try:
            with open(self.file_location + self.default_config_file, "w") as config_file:
                json.dump(self.value, config_file, indent=4)
        except IOError as e:
            if self.debug:
                print("Could not write configuration file")
            print(str(e))
            raise

    def good_place_for_file(self):
        # Figure out a good place to save the configuration file
        # I spent far too long figuring out if FreeBSD uses /home or /usr/home. Apparently
        # /home will be a symlink to /usr/home anyway so I decided to roll with that.
        #
        # Note: Linux = /home/user/, Freebsd = /home/user/ (symlink), OSX = /Users/user/
        my_platform = self.get_platform()
        if my_platform == "unix":
            return(str(os.path.expanduser("~")) + "/.config/" + self.app_name + "/")
        elif my_platform == "windows":
            return str(os.path.expanduser("~")) + "\\AppData\\Local\\" + self.app_name + "\\"
        else:
            return ""  # Fallback, return blank string so it saves in the current app location

    def get_platform(self):
        if platform.startswith("linux") or platform.startswith("freebsd") or platform.startswith("darwin"):
            return "unix"
        elif platform.startswith("win"):
            return "windows"
        else:
            return None




