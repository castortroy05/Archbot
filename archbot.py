from __future__ import annotations

from dataclasses import dataclass
from subprocess import CompletedProcess, run
from typing import Callable, Sequence


Executor = Callable[[Sequence[str]], CompletedProcess[str]]


@dataclass(frozen=True)
class ArchGuidance:
    trigger: str
    response: str


class ArchBot:
    """Minimal Arch Linux troubleshooting assistant."""

    def __init__(self, executor: Executor | None = None) -> None:
        self._executor = executor or self._run_command
        self._guidance = (
            ArchGuidance(
                "wifi",
                (
                    "Arch Wi-Fi troubleshooting: verify rfkill, list adapters with "
                    "`ip link`, scan with `iw dev`, and review NetworkManager logs via "
                    "`journalctl -u NetworkManager`. See: "
                    "https://wiki.archlinux.org/title/Network_configuration/Wireless"
                ),
            ),
            ArchGuidance(
                "boot",
                (
                    "Arch boot troubleshooting: check failed units with "
                    "`systemctl --failed`, review the current boot log with "
                    "`journalctl -b`, and verify bootloader config. See: "
                    "https://wiki.archlinux.org/title/General_troubleshooting"
                ),
            ),
            ArchGuidance(
                "package",
                (
                    "Arch package troubleshooting: sync package databases with "
                    "`sudo pacman -Sy`, inspect mirrors, and check package ownership "
                    "using `pacman -Qo <path>`. See: "
                    "https://wiki.archlinux.org/title/Pacman"
                ),
            ),
        )

    @staticmethod
    def _run_command(command: Sequence[str]) -> CompletedProcess[str]:
        return run(command, text=True, capture_output=True, check=False)

    def respond(self, user_input: str) -> str:
        normalized = user_input.strip().lower()
        if not normalized:
            return "Please describe your Arch Linux issue or request."

        for guidance in self._guidance:
            if guidance.trigger in normalized:
                return guidance.response

        if "disk" in normalized or "storage" in normalized:
            return self._format_command_response(("df", "-h"))
        if "memory" in normalized or "ram" in normalized:
            return self._format_command_response(("free", "-h"))
        if "services" in normalized or "failed units" in normalized:
            return self._format_command_response(("systemctl", "--failed"))

        return (
            "I can help troubleshoot Arch Linux. Try asking about Wi-Fi, boot, "
            "packages, disk usage, memory, or failed services."
        )

    def _format_command_response(self, command: Sequence[str]) -> str:
        completed = self._executor(command)
        if completed.returncode != 0:
            stderr = completed.stderr.strip() or "Unknown error"
            return f"Command {' '.join(command)} failed: {stderr}"
        stdout = completed.stdout.strip() or "(no output)"
        return f"Command output for {' '.join(command)}:\n{stdout}"


def main() -> None:
    bot = ArchBot()
    print("ArchBot: ask Arch Linux troubleshooting questions (type 'exit' to quit).")
    while True:
        try:
            user_input = input("> ")
        except EOFError:
            print("\nGoodbye.")
            break

        if user_input.strip().lower() in {"exit", "quit"}:
            print("Goodbye.")
            break

        print(bot.respond(user_input))


if __name__ == "__main__":
    main()
