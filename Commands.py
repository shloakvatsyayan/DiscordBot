
COMMAND_LIST = ["!ban ", "!hello ", "!ping"]


def has_command(message_contents: str):
    """
    TODO:
    You job is to change this function so that it does not always returns False and instead
    looks at the message_contents string and returns true if the message contents starts one
    of the commands listed in the command_list below. N
    Hints: Note that message_contents is a string.
    * If you need to check if this starts with another string, you may want to use startswith
    command as shown at https://www.geeksforgeeks.org/python-string-startswith/
    * You need to iterate over all elements of the list "command_list" and check if
    the message_content starts with it.
    :param message_contents:
    :return:
    """
    return False


def get_command_name(message_contents:str):
    contains_command = has_command(message_contents)
    if not contains_command:
        return None
    for each_command in COMMAND_LIST:
        if message_contents.startswith(each_command):
            return each_command

    return None


class BanCommand:
    def __init__(self, message_content:str):
        self.message_content = message_content
        self.argument = self._parse_argument()

    def _parse_argument(self):
        """
        TODO: You know that the command name is "!ban". you should
        find out the length of this string and then use that to find the substring
        that contains the name of the person to be banned. For example,
        self.message_contents could be "!ban shloak" . In this case, the length
        of "!ban" is 4. After that you have a single space. You should, therefore,
        get the part of self.message_contents starting from the 5 place all the way to the
        end. Do not try to make if the best  parsing function. Just do the simplest possible thing.
        Look up how to work with strings and in particular, string slices, at
        https://developers.google.com/edu/python/strings
        :return:
        """
        return ""

    def get_command_argument(self):
        return self.argument




