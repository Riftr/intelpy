import unittest
from intelpy.logging.logrotate import *


class TestCaseBase(unittest.TestCase):
    def assertFileExists(self, path):
        if not os.path.exists(path):
            raise AssertionError("File does not exist: " + str(path))


class TestLogRotate(unittest.TestCase):

    def test_large_debug_file(self):
        if os.path.exists("largetestfile.txt"):
            os.remove("largetestfile.txt")
        with open("largetestfile.txt", "wb") as f:
            size = 600  # bytes
            f.write((r"\0" * size).encode())
        self.assertTrue(check_log_size("largetestfile.txt", 100))

    def test_small_debug_file(self):
        if os.path.exists("smalltestfile.txt"):
            os.remove("smalltestfile.txt")
        with open("smalltestfile.txt", "wb") as f:
            size = 100  # bytes
            f.write((r"\0" * size).encode())
        self.assertFalse(check_log_size("smalltestfile.txt", 500))


class TestRotateFile(TestCaseBase):
    def test_rotate_log_file(self):
        if os.path.exists("testrotate_after.txt"):
            os.remove("testrotate_after.txt")
        with open("testrotate.txt", "wb") as f:
            size = 100  # bytes
            f.write((r"\0" * size).encode())
        path = "testrotate_after.txt"
        rotate_log_file("testrotate.txt", "testrotate_after.txt")
        self.assertFileExists(path)



if __name__ == '__main__':
        unittest.main()
