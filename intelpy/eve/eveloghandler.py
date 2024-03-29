from PyQt5.QtCore import pyqtSignal, QObject
from watchdog.events import PatternMatchingEventHandler
import pickle
from datetime import datetime
from itertools import islice
import re
import os
import intelpy.logging.logger


class EveLogHandler(PatternMatchingEventHandler, QObject):
    message_ready = pyqtSignal(list)

    def __init__(self, patterns=None, ignore_patterns=None,
                 ignore_directories=False, case_sensitive=False, configuration=None, logger=None):
        super(EveLogHandler, self).__init__()

        self.logger = logger

        # Update pattern so we only get files from the last 24 hours
        # we get */delve.imperium* etc
        # delve.imperium_20200207_151839.txt
        self._patterns = patterns
        self._ignore_patterns = ignore_patterns
        self._ignore_directories = ignore_directories
        self._case_sensitive = case_sensitive
        self.configuration = configuration
        self.known_msg_queue = []

        # Our variables
        # Known files
        self.known_files = {}
        self.known_files_loc = self.configuration.value["config_loc"] + "known_files.p"
        self.unpickle_known_files()
        self.maintain_known_files_file()  # Remove old files

        # This is valid python style regex now
        self.date_re = re.compile(r".\[\s(\d{4}\.\d{2}\.\d{2}\s\d{2}:\d{2}:\d{2})\s]")

        if configuration.value["debug"] and self.logger is not None:
            self.logger.write_log("Known files: " + str(self.known_files))
            for filename in self.known_files:
                self.logger.write_log(filename)


    def on_modified(self, event):
        # will fire on new files as well as modified files
        if self.configuration.value["debug"] and self.logger is not None:
            self.logger.write_log("Watchdog saw a file modified: " + str(event.src_path))
        # At this point, only files that match the filter will be available. Also,
        # they will have had an update to them. We need to get the file, compare to
        # our dict of files and figure out what line to process from. Once done, trigger
        # a Q signal to update the UI.
        #
        # event = FileModifiedEvent - fields: event_type (modified), is_directory, is_synthetic,
        #         tuple(3) - str "modified", str "file location", mystry bool "false"
        #         src_path = full file location (ie ./logs/delve.imperium_1234_1234.txt)

        if event.src_path not in self.known_files:
            # We got a new file, add it
            self.known_files[event.src_path] = 12     # Start at line 13 to avoid processing header
            self.pickle_dict()
        if self.configuration.value["debug"] and self.logger is not None:
            self.logger.write_log("Starting at line: " + str(self.known_files[event.src_path]))

        # get line/s from file
        try:
            with open(event.src_path, "r", encoding="utf_16_le") as file_data:
                new_lines = list(islice(file_data, self.known_files[event.src_path], None))

                for line in new_lines:
                    self.known_files[event.src_path] += 1
                    if self.configuration.value["debug"] and self.logger is not None:
                        print("Should be reading line " + str(self.known_files[event.src_path]))
                        self.logger.write_log("Should be reading line " + str(self.known_files[event.src_path]))

                    # check line against regex, if we get line with valid datetime string
                    if self.date_re.match(line):
                        new_parsed_msg = self.parse_message(line)
                        if self.configuration.value["debug"] and self.logger is not None:
                            self.logger.write_log("Got regex match: " + str(new_parsed_msg))

                        # Check for system msgs
                        if new_parsed_msg[1] == "EVE System":
                            if self.configuration.value["debug"] and self.logger is not None:
                                self.logger.write_log("Did not parse line, was system msg \n" + str(new_parsed_msg))
                            continue
                        # Check for old messages
                        present_time = datetime.utcnow()
                        past_time = new_parsed_msg[0]
                        gap_time = (present_time - past_time).total_seconds() / 60
                        if gap_time > self.configuration.value["message_timeout"]:
                            if self.configuration.value["debug"] and self.logger is not None:
                                self.logger.write_log("Did not parse line, was older than " + str(gap_time))
                                #self.logger.write_log(" " + new_parsed_msg)
                            continue
                        # Check if we've seen the line recently
                        if new_parsed_msg[1] + ">" + new_parsed_msg[2] in self.known_msg_queue:
                            if self.configuration.value["debug"] and self.logger is not None:
                                self.logger.write_log("Did not parse line, msg was seen recently")
                            continue
                        else:
                            # Add line to self.known_msg_queue and remove the oldest line
                            if len(self.known_msg_queue) > 10:
                                self.known_msg_queue.pop()
                            self.known_msg_queue.append(new_parsed_msg[1] + ">" + new_parsed_msg[2])
                            # Message should be good and unique, bubble up
                            self.message_ready.emit(new_parsed_msg)
                    else:
                        if self.configuration.value["debug"] and self.logger is not None:
                            self.logger.write_log("Line did not match date regex")

                self.pickle_dict()  # save file progress

        except IOError as e:
            if self.logger is not None:
                self.logger.write_log("Eveloghandler - Error reading Eve log file" + str(e))
            raise
        except Exception as err:
            if self.logger is not None:
                self.logger.write_log("Eveloghandler - Other error " + str(err))
            raise

    #def log_parsed_msg_list(self, reason, msgList):
    #    self.logger.write_log(reason)
    #    for line in msgList:
    #        self.logger.write_log(" - " + str(line))

    def maintain_known_files_file(self):
        # use on load, go though known files and clear out anything > 24 hrs
        remove_list = []

        for key in self.known_files.keys():
            if self.configuration.value["debug"] and self.logger is not None:
                self.logger.write_log("Maintain KF checking:" + str(key))
            try:
                file_date = str(key)[-19:-11]  # Get the date from the file name
                file_date_converted = datetime.strptime(file_date, "%Y%m%d")
            except ValueError as e:
                if self.configuration.value["debug"] and self.logger is not None:
                    self.logger.write_log("Error with known file data: " + str(e))
                remove_list.append(key)
                continue
            present_time = datetime.utcnow()
            gap_time = (present_time - file_date_converted).days
            if gap_time > 1:
                remove_list.append(key)

        for key_to_del in remove_list:
            if key_to_del in self.known_files:
                if self.configuration.value["debug"] and self.logger is not None:
                    self.logger.write_log("Maintain KF checking:" + str(key))
                try:
                    if self.configuration.value["debug"] and self.logger is not None:
                        self.logger.write_log("deleting key: " + str(key_to_del))
                    del self.known_files[key_to_del]
                except KeyError as e:
                    if self.configuration.value["debug"] and self.logger is not None:
                        self.logger.write_log("key error: " + str(e))

        self.pickle_dict()

    # Loads the known_files.p file
    # todo: move to json both pickle and unpickle functions due to dict usage
    # fix for now is to just skip and remove the corrupt file
    def unpickle_known_files(self):
        if os.path.exists(self.known_files_loc):
            if os.path.getsize(self.known_files_loc) > 0:
                try:
                    with open(self.known_files_loc, "rb") as known_files_file:
                        self.known_files = pickle.load(known_files_file)
                except Exception as e:
                    self.known_files = None
                    if self.configuration.value["debug"] and self.logger is not None:
                        self.logger.write_log("Couldn't load known_files.p, deleting corrupt file " +
                                              str(self.known_files_loc) +
                                              str(e))
                    try:
                        os.remove(self.known_files_loc)
                    except Exception as new_e:
                        if self.configuration.value["debug"] and self.logger is not None:
                            self.logger.write_log("Couldn't delete corrupt known_files.p. " +
                                                  str(self.known_files_loc) +
                                                  str(new_e))

    def pickle_dict(self):
        try:
            with open(self.known_files_loc, "wb") as known_files_file_pic:
                pickle.dump(self.known_files, known_files_file_pic)
        except Exception as e:
            if self.configuration.value["debug"] and self.logger is not None:
                self.logger.write_log("Couldn't save known_files.p, skipping. " + str(e))
            raise

    def print_known_file_list(self):
        for key, value in self.known_files.items():
            if self.configuration.value["debug"] and self.logger is not None:
                self.logger.write_log(key, value)

    def print_current_patterns(self):
        for value in self._patterns:
            if self.configuration.value["debug"] and self.logger is not None:
                self.logger.write_log(value)

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
            if self.configuration.value["debug"] and self.logger is not None:
                self.logger.write_log(
                    "Parsed line with DTS: " + message_list[0].strftime("%Y.%m.%d %H:%M:%S") +
                    "\n Nickname: " + message_list[1] +
                    "\n Message: " + message_list[2]
                )
            return message_list

        except Exception as e:
            if self.configuration.value["debug"] and self.logger is not None:
                self.logger.write_log(str(e))
            raise
