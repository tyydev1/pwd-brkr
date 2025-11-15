###################### pwd-brkr #####################
#                                                   #
#   pwd-brkr is a REPL made in Python for breaking  #
# a set of latin characters and arabic numerals.    #
#   It is not meant for password breaking.          #
#                                                   #
#####################################################

#####################
#   IMPORTS/SETUP   #
#####################

import getpass  # for hiding input and disabling echo
import os
import secrets
import sys
import threading
import time
from random import randint

from pyboxen import boxen
from rich import print as rprint
from rich.console import Console
from rich.markup import escape
from rich.table import Table
from rich.text import Text

try:
    sys.path.append(os.path.dirname(os.path.dirname(__file__)))
    from sandbox.sandbox import Sandbox

    SANDBOX_AVAILABLE = True
except (ImportError, ModuleNotFoundError):
    SANDBOX_AVAILABLE = False

    class Sandbox:
        def __init__(self, name):
            self.name = name
            self.is_sandbox_mode = False

        def init(self):
            pass

        def new_instance(self, name):
            pass

        def print(self, *args, **kwargs):
            print(*args)


pwd_brkr = Sandbox("pwd-brkr")
allowed_characters = [chr(i) for i in range(32, 127)]
console = Console()
loading_messages = [
    "Trying 'password123' again..",
    "Asking the password nicely..",
    "Reading the sticky note under the keyboard..",
    "Compiling the password from source..",
    "sudo give-me-password --please",
    "Checking if it's 'admin'..",
    "Consulting Stack Overflow..",
    "Works on my machine..",
    "Adding more print statements..",
    "Reticulating splines..",
    "It's not a bug, it's a feature..",
    "TODO: Optimize this later..",
    "Powered by caffeine and desperation..",
    "99 little bugs in the code..",
    "Have you tried turning it off and on again?",
    "This will only take a second.. or several thousand..",
    "Dividing by zero for luck..",
    "Sacrificing a rubber duck to the code gods..",
    "Googling 'how to hack password python'..",
    "Pressing F to pay respects..",
    "git commit -m 'fix stuff'..",
    "Invoking the ancient algorithm of trial and error..",
]

###############

###############


class SpinnerThread(threading.Thread):
    def __init__(
        self,
        console: Console,
        messages: list,
        message_delay: float = 5.0,
        frame_tick: float = 0.08,
        frames: list = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"],
    ):
        super().__init__()
        self._stop_event = threading.Event()
        self.console = console
        self.messages = messages if messages else ["Loading..."]
        self.daemon = True

        self.spinner_frame = frames[:]
        self.frame_speed = frame_tick
        self.message_delay = message_delay
        self._lock = threading.Lock()

    def stop(self):
        self._stop_event.set()

    def run(self):
        try:
            i = 0
            msg_idx = 0
            last_msg_switch = time.time()

            max_len = max(len(m) for m in self.messages) if self.messages else 20

            DIM = "\033[2m"
            RESET = "\033[0m"

            while not self._stop_event.is_set():
                with self._lock:
                    current_msg = self.messages[msg_idx]
                    current_frame = self.spinner_frame[i % len(self.spinner_frame)]

                    output = f"{current_frame} {current_msg}"

                    padded_output = output.ljust(max_len + 2)
                    sys.stdout.write(f"\r{DIM}{padded_output}{RESET}")
                    sys.stdout.flush()

                if time.time() - last_msg_switch >= self.message_delay:
                    msg_idx = (msg_idx + 1) % len(self.messages)
                    last_msg_switch = time.time()

                time.sleep(self.frame_speed)
                i += 1

            with self._lock:
                sys.stdout.write("\r" + " " * (max_len + 2) + "\r")
                sys.stdout.flush()
        except Exception as e:
            pass


###################


def pwd_break(
    pwd: str,
    with_rate_limit: bool = False,
    set_rate_limit=None,
    rate_cooldown=5,
    show_detail: bool = False,
):
    if not pwd:
        rprint("[red][x] ERROR: Empty password provided[/red]")
        return

    try:
        break_attempt = ""
        effective_rate_limit = set_rate_limit
        access_count = 0

        spinner = SpinnerThread(console, loading_messages, frames=allowed_characters)
        spinner.start()

        for position in range(len(pwd)):
            if (
                effective_rate_limit is not None
                and access_count >= effective_rate_limit
            ):
                spinner.stop()
                spinner.join(timeout=1.0)

                rprint(
                    f"\n[magenta][!] RATE LIMIT EXCEEDED - Cooldown: {rate_cooldown}s[/magenta]"
                )
                access_count = 0
                time.sleep(rate_cooldown)

                spinner = SpinnerThread(console, loading_messages)
                spinner.start()

            for char in allowed_characters:
                candidate_char = break_attempt + char

                # styled = Text()

                # if break_attempt:
                #     styled.append(break_attempt, style="dim bright_green")

                # if pwd.startswith(candidate_char):
                #     styled.append(char, style="bold bright_green")
                # else:
                #     styled.append(char, style="dim white strike")

                # live.update(styled)

                access_count += 1

                if pwd.startswith(candidate_char):
                    break_attempt += char
                    break

            if break_attempt == pwd:
                break

        spinner.stop()
        spinner.join(timeout=1.0)

        rprint("[bold bright_green][+] Cracked stringset. [/bold bright_green]")

    except KeyboardInterrupt:
        spinner.stop()
        spinner.join(timeout=1.0)
        rprint("\n[yellow][!] Cracking interrupted by user[/yellow]")
    except Exception as e:
        if "spinner" in locals():
            spinner.stop()
            spinner.join(timeout=1.0)
        rprint(f"[red][x] ERROR during cracking: {str(e)}[/red]")


def handle_cmd(cmd: str):
    if not cmd or cmd.isspace():
        return None

    try:
        if cmd.startswith("exit"):
            if cmd.endswith(" --help") or cmd.endswith(" -h"):
                rprint("[bright_yellow][?] Usage: exit[/bright_yellow]")
                rprint("[dim white]    Terminates the pwd-brkr session[/dim white]\n")
                return None
            rprint("[dim cyan][-] Terminating session...[/dim cyan]")
            sys.exit(0)

        elif cmd.startswith("random-break") or cmd.startswith("randbreak"):
            args = cmd.split()
            min_len = 8
            max_len = 50
            rate_limit = None
            rate_cooldown = 5
            default = len(args) == 1

            if cmd.endswith(" --help") or cmd.endswith(" -h"):
                rprint(
                    "[bright_yellow][?] Usage: random-break <max (if alone) else min>? <max>? <rate_limit>? <rate_limit_cooldown>?[/bright_yellow]\n"
                )
                return None

            try:
                if len(args) == 2:
                    max_len = int(args[1])
                    if max_len < 1:
                        raise ValueError("Max length must be positive")
                elif len(args) == 3:
                    min_len = int(args[1])
                    max_len = int(args[2])
                    if min_len < 1 or max_len < min_len:
                        raise ValueError("Invalid min/max range")
                elif len(args) == 4:
                    min_len = int(args[1])
                    max_len = int(args[2])
                    rate_limit = int(args[3])
                    if min_len < 1 or max_len < min_len:
                        raise ValueError("Invalid min/max range")
                    if rate_limit < 1:
                        raise ValueError("Rate limit must be positive")
                elif len(args) == 5:
                    min_len = int(args[1])
                    max_len = int(args[2])
                    rate_limit = int(args[3])
                    rate_cooldown = int(args[4])
                    if min_len < 1 or max_len < min_len:
                        raise ValueError("Invalid min/max range")
                    if rate_limit < 1:
                        raise ValueError("Rate limit must be positive")
                    if rate_cooldown < 0:
                        raise ValueError("Cooldown must be non-negative")
                elif len(args) > 5:
                    rprint(
                        "[red][x] ERROR: Too many arguments. Use --help for usage info.[/red]"
                    )
                    return None

            except ValueError as e:
                rprint(f"[red][x] ERROR: Invalid argument - {str(e)}[/red]")
                rprint(
                    "[dim white]    Use --help flag for usage information[/dim white]"
                )
                return None

            try:
                length = randint(min_len, max_len)
                random_pwd = "".join(
                    secrets.choice(allowed_characters) for _ in range(length)
                )
                # Escape the password to prevent Rich markup interpretation
                escaped_pwd = escape(random_pwd)
                rprint(
                    f"[bright_yellow][*] TARGET GENERATED: {escaped_pwd}[/bright_yellow]"
                )
                rprint(f"[dim white]    Length: {length} characters[/dim white]\n")
            except Exception as e:
                rprint(f"[red][x] ERROR: Failed to generate password - {str(e)}[/red]")
                return None

            try:
                confirmation = (
                    input("[>] Initiate crack sequence (y/n)? ").strip().lower()
                )
                print()
            except (EOFError, KeyboardInterrupt):
                rprint("\n[yellow][!] Input cancelled[/yellow]")
                return None

            if confirmation == "y":
                pwd_break(
                    random_pwd, set_rate_limit=rate_limit, rate_cooldown=rate_cooldown
                )
                print()
            elif confirmation == "n":
                rprint("[dim cyan][-] Crack sequence cancelled[/dim cyan]")
            else:
                rprint("[yellow][!] Invalid response - cancelled[/yellow]")

        elif cmd.startswith("break"):
            args = cmd.split()

            if len(args) < 2:
                rprint("[red][x] ERROR: Need a stringset for the second argument.")
                return None

            pwd_break(args[1])

        elif cmd.startswith("try-printallowedchar") or cmd.startswith("chars"):
            if cmd.endswith(" --help") or cmd.endswith(" -h"):
                rprint("[bright_yellow][?] Usage: try-printallowedchar[/bright_yellow]")
                rprint(
                    "[dim white]    Displays the full character set used for cracking[/dim white]\n"
                )
                return None
            rprint(
                f"[bright_cyan][*] Allowed character set ({len(allowed_characters)} chars):[/bright_cyan]"
            )
            # Escape the character list to prevent Rich markup interpretation
            escaped_chars = escape(str(allowed_characters))
            rprint(escaped_chars)
            print()

        elif cmd.startswith("clear") or cmd.startswith("cls"):
            if cmd.endswith(" --help") or cmd.endswith(" -h"):
                rprint("[bright_yellow][?] Usage: clear[/bright_yellow]")
                rprint("[dim white]    Clears the screen[/dim white]\n")
                return None

            os.system("clear")

        elif cmd.startswith("list") or cmd.startswith("ls"):
            if cmd.endswith(" --help") or cmd.endswith(" -h"):
                rprint("[bright_yellow][?] Usage: list[/bright_yellow]")
                rprint(
                    "[dim white]    Displays all available commands with usage info[/dim white]\n"
                )
                return None

            print()
            list_of_commands = Table(
                title="[COMMAND REGISTRY]", title_style="bold bright_cyan"
            )
            list_of_commands.add_column("#", style="dim white", no_wrap=True)
            list_of_commands.add_column("Command", style="bright_cyan")
            list_of_commands.add_column("Arguments", style="bright_yellow")
            list_of_commands.add_column("Description", style="dim white")

            list_of_commands.add_row(
                "1",
                "random-break",
                "<max>\n<min> <max>\n<min> <max> <rate>\n<min> <max> <rate> <cd>",
                "Generate & crack random stringset\nUse --help for details",
            )
            list_of_commands.add_row(
                "2", "try-printallowedchar", "(none)", "Display allowed character set"
            )
            list_of_commands.add_row(
                "3", "list", "(none)", "Show this command registry"
            )
            list_of_commands.add_row("4", "exit", "(none)", "Terminate session")
            console.print(list_of_commands)
            print()

        else:
            rprint(f"[red][x] UNKNOWN COMMAND: '{cmd}'[/red]")

    except KeyboardInterrupt:
        rprint("\n[yellow][!] Command interrupted[/yellow]")
        return None
    except Exception as e:
        rprint(f"[red][x] ERROR: Unexpected error - {str(e)}[/red]")
        return None

    return None


#################
# REPL          #
#################


def main():
    try:
        prompt = Text("[pwd-brkr] # ", style="bright_cyan")
        prompt.stylize("bright_white", 11, 13)

        print(
            boxen(
                """
[bright_cyan]
                ██████╗>██╗>>>>██╗██████╗>>>>>>>██████╗>██████╗>██╗>>██╗██████╗>
                ██╔══██╗██║>>>>██║██╔══██╗>>>>>>██╔══██╗██╔══██╗██║>██╔╝██╔══██╗
                ██████╔╝██║>█╗>██║██║>>██║█████╗██████╔╝██████╔╝█████╔╝>██████╔╝
                ██╔═══╝>██║███╗██║██║>>██║╚════╝██╔══██╗██╔══██╗██╔═██╗>██╔══██╗
                ██║>>>>>╚███╔███╔╝██████╔╝>>>>>>██████╔╝██║>>██║██║>>██╗██║>>██║
                ╚═╝>>>>>>╚══╝╚══╝>╚═════╝>>>>>>>╚═════╝>╚═╝>>╚═╝╚═╝>>╚═╝╚═╝>>╚═╝
[/bright_cyan][bright_white]
                                pwd-brkr v0.7 - dev.release
[/bright_white][dim white]
        pwd-brkr is a clean stringset (basically password) guessing machine that's highly customizable and is aesthetically beautiful. developer version.
[/dim white]
""",
                style="double",
                text_alignment="center",
                color="cyan",
            )
        )
        rprint(
            "[dim white][*] Type 'list' for available commands | Use --help flag for command info | 'exit' to quit[/dim white]\n"
        )

        while True:
            try:
                rprint(prompt, end="")
                user_cmd = input().strip()

                handle_cmd(user_cmd)

            except KeyboardInterrupt:
                rprint("\n[yellow][!] Use 'exit' command to quit[/yellow]")
                continue
            except EOFError:
                rprint("\n[dim cyan][-] Terminating session...[/dim cyan]")
                break
            except Exception as e:
                rprint(f"\n[red][x] REPL ERROR: {str(e)}[/red]")
                continue

    except Exception as e:
        rprint(f"[red][x] FATAL ERROR: {str(e)}[/red]")
        sys.exit(1)


if __name__ == "__main__" and not pwd_brkr.is_sandbox_mode:
    main()


###############
#   SANDBOX   #
###############

if pwd_brkr.is_sandbox_mode:
    try:
        pwd_brkr.init()
        pwd_brkr.new_instance("Rich With rprint")

        nums_list = [1, 2, 3, 4, 5]
        rprint(nums_list)

        nums_tuple = (1, 2, 3, 4)
        rprint(nums_tuple)

        nums_dict = {"nums_list": nums_list, "nums_tuple": nums_tuple}
        rprint(nums_dict)

        bool_list = [True, False]
        rprint(bool_list)

        print()
        pwd_brkr.print("Done testing!", color="dim", detailed_mode=True)

        pwd_brkr.new_instance("Carriage")

        rprint("YO", end="\r")
        time.sleep(1)
        rprint("HEY")
    except Exception as e:
        rprint(f"[red][x] Sandbox error: {str(e)}[/red]")
