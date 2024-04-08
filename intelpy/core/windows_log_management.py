import os
import shutil

# additional handling for Windows platform
# NTFS does not provide notifications of file changes
# like Linux file systems so we have to go to more effort
# to minimise resource usage


def windows_archive_eve_logs(chatlog_loc, logger=None):
    if logger is not None:
        print("Archiving old logs (Windows)")
    archive_path = os.path.join(os.path.expanduser("~"), "Documents", "Eve", "Log Archive")
    files_found_count = 0
    files_archived_count = 0
    # Create archive path if it doesn't exist
    if not os.path.exists(archive_path):
        try:
            if logger is not None:
                print("Making " + str(archive_path))
                logger.write_log("Making archive path for old logs: " + str(archive_path))
                print("Making archive path for old logs: " + str(archive_path))
            os.makedirs(archive_path)
        except IOError as e:
            if logger is not None:
                logger.write_log("Could not create log archive path! " + str(archive_path))
                print("Could not create log archive path! " + str(archive_path))
            print(str(e))
            raise

    # Move old logs
    current_files = os.listdir(chatlog_loc)
    for file in current_files:
        files_found_count += 1
        if file.lower().endswith(".txt"):  # safeguard to only target .txt files
            try:
                if os.path.exists(archive_path + "\\" + file):
                    if logger is not None:
                        print("Archive path file already existed, skipping")
                        logger.write_log("Archive path file already existed, skipping")
                else:
                    files_archived_count += 1
                    shutil.move(chatlog_loc + "\\" + file, archive_path)
            except IOError as e:
                if logger is not None:
                    print(e)
                    logger.write_log("Log file was in use while archiving, probably by Eve. Skipping file")
                continue

    if logger is not None:
        print("Archive found " + str(files_found_count) + " files.")
        print("Archive should have moved " + str(files_archived_count) + " files.")
        logger.write_log("Archive: Found " + str(files_found_count) + " files.")
        logger.write_log("Archive: Should have moved " + str(files_archived_count) + " files.")