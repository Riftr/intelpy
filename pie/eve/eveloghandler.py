from PyQt5.QtCore import pyqtSignal, QObject
from watchdog.events import PatternMatchingEventHandler
import pickle
from pathlib import Path
from datetime import datetime
import re


class EveLogHandler(PatternMatchingEventHandler, QObject):
    message_ready = pyqtSignal(list)

    def __init__(self, patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False, configuration=None):
        super(EveLogHandler, self).__init__()

        # Update pattern so we only get files from the last 24 hours
        # we get */delve.imperium* etc
        # delve.imperium_20200207_151839.txt
        self._patterns = patterns

        self._ignore_patterns = ignore_patterns
        self._ignore_directories = ignore_directories
        self._case_sensitive = case_sensitive
        self.configuration = configuration


        # Our variables
        self.known_files = {}
        self.known_files_loc = self.configuration.value["config_loc"] + "known_files.p"
        # Todo: clear this of files > 24 hours old to keep size in check
        # Todo: also save it more frequently in case problems?
        self.load_known_files()

    def on_modified(self, event):
        # will fire on new files as well as modified files
        if self.configuration.value["debug"]:
            print("Watchdog saw a file modified")
        # At this point, only files that match the filter will be available. Also,
        # they will have had an update to them. We need to get the file, compare to
        # our dict of files and figure out what line to process from. Once done, trigger
        # a Q signal to update the UI.
        #
        # event = FileModifiedEvent - fields: event_type (modified), is_directory, is_synthetic,
        #         tuple(3) - str "modified", str "file location", mystry bool "false"
        #         src_path = full file location (ie ./logs/delve.imperium_1234_1234.txt)

        #return_list = []

        if event.src_path not in self.known_files.keys():
            # We got a new file, add it
            self.known_files[event.src_path] = 13     # Start at line 13 to avoid processing header

        if self.configuration.value["debug"]:
            print("Starting at line: " + str(self.known_files[event.src_path]))

        # get line/s from file
        try:
            with open(event.src_path, "r", encoding="utf_16_le") as file_data:

                all_lines = file_data.readlines()
                if len(all_lines) < 13:
                    if self.configuration.value["debug"]:
                        print("file had less than 13 lines. Either is just a header file or not a chat log")
                    return
                else:
                    # instead of reading all lines ever time, lets try to read from where we left off
                    diff_line = len(all_lines) - self.known_files[event.src_path]
                    process_list = all_lines[-diff_line:]
                    self.known_files[event.src_path] += len(process_list)  # add how many lines we read in
                    self.pickle_dict()

                    for raw_line in process_list:  # check lines and remove DTS > 10 mins or so

                        if not raw_line[1] == "[":
                            if self.configuration.value["debug"]:
                                print("line was not processed as it did not start with [")
                                print("last line 0 is: " + raw_line[0])
                                print("last line 1 is: " + raw_line[1])
                                print("last line 2 is: " + raw_line[2])
                            #return
                        else:
                            parsed_line = self.parse_message(raw_line)
                            if not parsed_line[1] == "EVE System":   # Chucking away this for now, will use one day
                                #self.pickle_dict()  # Save our known lines file (was a test)

                                present_time = datetime.utcnow()
                                past_time = parsed_line[0]
                                gap_time = (present_time - past_time).total_seconds() / 60
                                if gap_time > self.configuration.value["message_timeout"]:
                                    # message was old. Not sure if we care about remembering lines now
                                    if self.configuration.value["debug"]:
                                        print("message was old, ignoring")
                                    #return
                                # 4th item in list, how many lines were unknown
                                else:
                                    if len(process_list) > 1:
                                        parsed_line.append(len(process_list))
                                        if self.configuration.value["debug"]:
                                            print("more than 1 line was unknown")
                                            print(process_list)
                                    else:
                                        parsed_line.append(0)
                                    self.message_ready.emit(parsed_line)
                            else:
                                if self.configuration.value["debug"]:
                                    print("line was not processed, was an eve system msg")

        except IOError as e:
            print("Error reading Eve log file" + str(e))
            raise

    def maintain_known_files_file(self):
        # use on load, go though known files and clear out anything > 24 hrs
        for key in self.known_files.keys():
            str(key).split("_", 1)


    #def load_known_files(self):
    #    if Path(self.known_files_loc).exists():
    #       self.unpickle_dict()

    def unpickle_dict(self):
        if Path(self.known_files_loc).exists():
            with open(self.known_files_loc, "rb") as ku:
                self.known_files = pickle.load(ku)

    def pickle_dict(self):
        with open(self.known_files_loc, "wb") as kp:
            pickle.dump(self.known_files, kp)

    def print_known_file_list(self):
        for key, value in self.known_files.items():
            print(key, value)

    def print_current_patterns(self):
        for value in self._patterns:
            print(value)

    def update_patterns(self, new_patterns):
        self._patterns = new_patterns

    # Parse the message we got from our log, return list with 3 items (DTS, nickname, message)
    def parse_message(self, line):
        try:
            # Split line up
            message_list = []
            split_line = line.split(" ] ", 1)        # initial split

            # Add pieces to our list (datetime, nickname, message)
            dts = split_line[0].split("[ ", 1)[1]         # DTS
            # convert to datetime object
            dts_converted = datetime.strptime(dts, "%Y.%m.%d %H:%M:%S")
            message_list.append(dts_converted)
            nick_and_msg = split_line[1].split(" > ", 1)   # split nick and message up
            message_list.append(nick_and_msg[0])  # nickname
            message_list.append(nick_and_msg[1])  # message
            if self.configuration.value["debug"]:
                print("----")
                print("parsing line: " + line)
                print("DTS: " + message_list[0].strftime("%Y.%m.%d %H:%M:%S"))
                print("Nickname: " + message_list[1])
                print("Message: " + message_list[2])

            return message_list

        except Exception as e:
            raise
