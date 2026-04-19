import unittest
from subprocess import CompletedProcess
from typing import Sequence

from archbot import ArchBot


class ArchBotTests(unittest.TestCase):
    def test_wifi_guidance_contains_archwiki_link(self) -> None:
        bot = ArchBot()
        response = bot.respond("my wifi keeps disconnecting")
        self.assertIn("Arch Wi-Fi troubleshooting", response)
        self.assertIn("wiki.archlinux.org", response)

    def test_disk_and_storage_requests_run_allowlisted_command(self) -> None:
        captured: list[Sequence[str]] = []

        def fake_executor(command: Sequence[str]) -> CompletedProcess[str]:
            captured.append(command)
            return CompletedProcess(command, 0, stdout="Filesystem data", stderr="")

        bot = ArchBot(executor=fake_executor)
        response_disk = bot.respond("check disk usage")
        response_storage = bot.respond("show storage usage")
        self.assertEqual(captured, [("df", "-h"), ("df", "-h")])
        self.assertIn("Filesystem data", response_disk)
        self.assertIn("Filesystem data", response_storage)

    def test_command_failure_is_reported(self) -> None:
        def fake_executor(command: Sequence[str]) -> CompletedProcess[str]:
            return CompletedProcess(command, 1, stdout="", stderr="permission denied")

        bot = ArchBot(executor=fake_executor)
        response = bot.respond("show memory")
        self.assertIn("failed", response)
        self.assertIn("permission denied", response)


if __name__ == "__main__":
    unittest.main()
