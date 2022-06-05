import time
import unittest

import user
import user as u
import time as t
import pytest
import threading


class TestUserAccount(unittest.TestCase):

    def test_threading(self):

        t = threading.Thread(target=self.thread_function, args=None)

        t.start()
        t.join()

    def thread_function(self):
        while True:
            print("Hello")
            time.sleep(1)


if __name__ == '__main__':
    unittest.main()
