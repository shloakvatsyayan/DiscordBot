import unittest
import not_allowed_words as n


class TestOterlu(unittest.TestCase):
    def test_badword(self):
        message = "shut up"
        labels = n.check_message(message)
        print(labels)


if __name__ == '__main__':
    unittest.main()
