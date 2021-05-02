import unittest
import Commands


class TestCommandFunctions(unittest.TestCase):
    def test_has_command(self):
        message_content = "!ban shloak"
        output = Commands.has_command(message_content)
        self.assertTrue(output, "Should have returned true for !ban shloak but your function returned false!")

    def test_ban_command(self):
        message_content = "!ban Shloak"
        ban_cmd = Commands.BanCommand(message_content)
        cmd_arg = ban_cmd.get_command_argument()
        self.assertEqual("Shloak", cmd_arg, "you have not implemented the function properly!")


if __name__ == '__main__':
    unittest.main()
