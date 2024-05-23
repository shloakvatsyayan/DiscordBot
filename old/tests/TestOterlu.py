import unittest
import not_allowed_words as n


class TestOterlu(unittest.TestCase):
    def test_badword(self):
        message = "shut up"
        labels = n.check_message(message)
        print(labels)
        labels_dict = {}
        for d in labels:
            labels_dict[d['label']] = d['level']
        print(labels_dict)
        if labels_dict["TOXIC"] == 3:
            print("Success")


if __name__ == '__main__':
    unittest.main()
