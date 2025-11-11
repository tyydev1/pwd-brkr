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
from random import randint
from time import sleep

from pyboxen import boxen
from rich import print as rprint
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.text import Text

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sandbox.sandbox import Sandbox

pwd_brkr = Sandbox("pwd-brkr")
allowed_characters = [chr(i) for i in range(32, 127)]
console = Console()

###############


def pwd_break(
    pwd: str, with_rate_limit: bool = False, set_rate_limit=None, rate_cooldown=5
):
    break_attempt = ""
    with_rate_limit = True if set_rate_limit is not None else False
    rate_limit = set_rate_limit if with_rate_limit else None
    access_count = 0

    with Live(console=console, refresh_per_second=20) as live:
        for _ in range(len(pwd)):
            if rate_limit is not None and access_count >= rate_limit:
                rprint(
                    f"\n[magenta][!] RATE LIMIT EXCEEDED - Cooldown: {rate_cooldown}s[/magenta]"
                )
                access_count = 0
                sleep(rate_cooldown)
            for char in allowed_characters:
                candidate_char = break_attempt + char

                styled = Text()

                if break_attempt:
                    styled.append(break_attempt, style="bright_cyan")

                if pwd.startswith(candidate_char):
                    styled.append(char, style="bright_cyan")
                else:
                    styled.append(char, style="dim white strike")

                # remaining_len = size - len(candidate_char)
                # if remaining_len > 0:
                #     styled.append("_" * remaining_len, style="dim white")

                live.update(styled)

                access_count += 1
                if pwd.startswith(candidate_char):
                    break_attempt += char
                    break

            if break_attempt == pwd:
                break

        # Show final success message
        live.update(Text(f"[+] CRACKED: {break_attempt}\n", style="bold bright_green"))


def handle_cmd(cmd: str):
    if cmd.startswith("exit"):
        if cmd.endswith(" --help") or cmd.endswith(" -h"):
            rprint("[bright_yellow][?] Usage: exit[/bright_yellow]")
            rprint("[dim white]    Terminates the pwd-brkr session[/dim white]\n")
            return None
        rprint("[dim cyan][-] Terminating session...[/dim cyan]")
        exit()

    # try #
    elif cmd.startswith("random-break"):
        args = cmd.split()
        default = False
        min = 8
        max = 50
        rate_limit = None
        rate_cooldown = 5
        is_help = False
        default = True if len(args) == 1 else False

        if cmd.endswith(" --help") or cmd.endswith(" -h"):
            rprint(
                "[bright_yellow][?] Usage: random-break <max (if alone) else min>? <max>? <rate_limit>? <rate_limit_cooldown>?[/bright_yellow]\n"
            )
            is_help = True

        if is_help:
            return None

        if len(args) == 2:
            min = 8
            max = int(args[1])
        elif len(args) == 3:
            min = int(args[1])
            max = int(args[2])
        elif len(args) == 4:
            min = int(args[1])
            max = int(args[2])
            rate_limit = int(args[3])
        elif len(args) == 5:
            min = int(args[1])
            max = int(args[2])
            rate_limit = int(args[3])
            rate_cooldown = int(args[4])
        elif len(args) > 5 and not default:
            rprint("[red][x] ERROR: Too many arguments.[/red]")

        length = randint(min, max)
        random_pwd = "".join(secrets.choice(allowed_characters) for _ in range(length))
        rprint(f"[bright_yellow][*] TARGET GENERATED: {random_pwd}\n[/bright_yellow]")
        confirmation = input("[>] Initiate crack sequence (y/n)? ")

        if confirmation.lower() == "y":
            pwd_break(
                random_pwd, set_rate_limit=rate_limit, rate_cooldown=rate_cooldown
            )

    elif cmd.startswith("try-printallowedchar"):
        if cmd.endswith(" --help") or cmd.endswith(" -h"):
            rprint("[bright_yellow][?] Usage: try-printallowedchar[/bright_yellow]")
            rprint("[dim white]    Displays the full character set used for cracking[/dim white]\n")
            return None
        rprint(allowed_characters)

    elif cmd.startswith("list"):
        if cmd.endswith(" --help") or cmd.endswith(" -h"):
            rprint("[bright_yellow][?] Usage: list[/bright_yellow]")
            rprint("[dim white]    Displays all available commands with usage info[/dim white]\n")
            return None

        print()
        list_of_commands = Table(title="[COMMAND REGISTRY]", title_style="bold bright_cyan")
        list_of_commands.add_column("#", style="dim white", no_wrap=True)
        list_of_commands.add_column("Command", style="bright_cyan")
        list_of_commands.add_column("Arguments", style="bright_yellow")
        list_of_commands.add_column("Description", style="dim white")

        list_of_commands.add_row(
            "1",
            "random-break",
            "<max>\n<min> <max>\n<min> <max> <rate>\n<min> <max> <rate> <cd>",
            "Generate & crack random stringset\nUse --help for details"
        )
        list_of_commands.add_row("2", "try-printallowedchar", "(none)", "Display allowed character set")
        list_of_commands.add_row("3", "list", "(none)", "Show this command registry")
        list_of_commands.add_row("4", "exit", "(none)", "Terminate session")
        console.print(list_of_commands)
        print()
        

    elif cmd == "":
        return None
    else:
        rprint(f"[red][x] UNKNOWN COMMAND: '{cmd}'[/red]")


#################
# REPL          #
#################

user_cmd = None

if __name__ == "__main__" and not pwd_brkr.is_sandbox_mode:
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
                                pwd-brkr v0.2 - dev.release
[/bright_white][dim white]
        pwd-brkr is a clean stringset (basically password) guessing machine that's highly customizable and is aesthetically beautiful. developer version.
[/dim white]
""",
            style="double",
            text_alignment="center",
            color="cyan",
        )
    )
    rprint("[dim white][*] Type 'list' for available commands | Use --help flag for command info | 'exit' to quit[/dim white]\n")
    while True:
        rprint(prompt, end="")
        user_cmd = input().strip()
        result = handle_cmd(user_cmd)


###############
#   SANDBOX   #
###############

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
sleep(1)
rprint("HEY")
