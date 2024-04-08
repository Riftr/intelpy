import getpass
import os


def find_eve_chatlogs_dir(platform, logger=None):
    if platform == "unix":
        if logger is not None:
            logger.write_log("Detected OS was Unix")

        lutris_path = os.path.join(os.path.expanduser("~"),
                                   "Games",
                                   "eve-online",
                                   "drive_c",
                                   "users",
                                   getpass.getuser(),
                                   "My Documents",
                                   "EVE",
                                   "logs",
                                   "Chatlogs")
        steam_path = os.path.join(os.path.expanduser("~"),
                                  ".local",
                                  "share",
                                  "Steam",
                                  "steamapps",
                                  "compatdata",
                                  "8500",
                                  "pfx",
                                  "drive_c",
                                  "users",
                                  "steamuser",
                                  "My Documents",
                                  "EVE",
                                  "logs",
                                  "Chatlogs")

        if os.path.exists(steam_path):
            return str(steam_path)
        elif os.path.exists(lutris_path):
            return str(lutris_path)
    elif platform == "windows":
        if logger is not None:
            logger.write_log("Detected OS was Windows")
        home_path = os.path.expanduser("~")
        test_path = os.path.join(home_path, "Documents", "EVE", "logs", "Chatlogs")
        test_path_odrive = os.path.join(home_path, "OneDrive", "Documents", "EVE", "logs", "Chatlogs")
        # Check default path on windows
        if check_path(test_path):
            return str(test_path)
        # Check if its on Onedrive instead
        elif check_path(test_path_odrive):
            return str(test_path_odrive)
    else:
        if logger is not None:
            logger.write_log("Unsupported OS or could not detect OS")
    # if we get to here we couldn't find the path
    if logger is not None:
        logger.write_log("Could not determine Eve log path!")
    return None


def check_path(test_path):
    if os.path.exists(test_path):
        return True
    else:
        return False
