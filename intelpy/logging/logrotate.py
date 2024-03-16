import os


def check_log_size(log_file, max_size=5242880):
    if os.path.exists(log_file):
        file_info = os.stat(log_file)
        if file_info.st_size > max_size:
            return True
    return False


def rotate_log_file(log_file_full_path, to_name):
    if os.path.exists(to_name):
        os.remove(to_name)
    os.rename(log_file_full_path, to_name)
