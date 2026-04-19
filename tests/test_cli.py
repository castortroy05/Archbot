import io
import unittest
from contextlib import redirect_stdout

from archbot.cli import main


class TestCLI(unittest.TestCase):
    def test_main_prints_scaffold_message(self) -> None:
        stream = io.StringIO()
        with redirect_stdout(stream):
            main()
        self.assertEqual(stream.getvalue().strip(), "Archbot scaffold is ready.")


if __name__ == "__main__":
    unittest.main()

