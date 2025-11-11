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
                    f"\n[red][Fail] Reached rate limit. Resetting in {rate_cooldown} seconds.[/red]"
                )
                access_count = 0
                sleep(rate_cooldown)
            for char in allowed_characters:
                candidate_char = break_attempt + char

                styled = Text()

                if break_attempt:
                    styled.append(break_attempt, style="dim green")

                if pwd.startswith(candidate_char):
                    styled.append(char, style="dim green")
                else:
                    styled.append(char, style="red undeline")

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
        live.update(Text(f"Found stringset: {break_attempt}", style="bold green"))


def handle_cmd(cmd: str):
    if cmd == "exit":
        rprint("[dim]Exiting pwd-brkr.. Goodbye! [/dim]")
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
                "[yellow]Usage: random-break <max (if alone) else min>? <max>? <rate_limit>? <rate_limit_cooldown>?[/yellow]\n"
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
            rprint("[red]try-break: Too many arguments.[/red]")

        length = randint(min, max)
        random_pwd = "".join(secrets.choice(allowed_characters) for _ in range(length))
        rprint(f"[yellow]The random password generated is: {random_pwd}\n[/yellow]")
        confirmation = input("Continue (y/n)?  ")

        if confirmation.lower() == "y":
            pwd_break(
                random_pwd, set_rate_limit=rate_limit, rate_cooldown=rate_cooldown
            )

    elif cmd == "try-printallowedchar":
        rprint(allowed_characters)

    elif cmd == "list":
        print()
        list_of_commands = Table(title="List Of Commands")
        list_of_commands.add_column("No.", style="white", no_wrap=True)
        list_of_commands.add_column("Command", style="cyan")
        list_of_commands.add_column("Usage", style="yellow")
        list_of_commands.add_column("Action", style="dim")
        
        list_of_commands.add_row("0", "unknown", "none", "Default action")
        list_of_commands.add_row("1", "unknown", "none", "Default action")
        list_of_commands.add_row("2", "unknown", "none", "Default action")
        list_of_commands.add_row("3", "unknown", "none", "Default action")
        list_of_commands.add_row("4", "unknown", "none", "Default action")
        console.print(list_of_commands)
        rprint("[yellow]Sorry, that's not available right now :/\n[/yellow]")
        

    elif cmd == "":
        return None
    else:
        rprint(f"'{cmd}' is not a knowd pwd-brkr command.")


#################
# REPL          #
#################

user_cmd = None

if __name__ == "__main__" and not pwd_brkr.is_sandbox_mode:
    prompt = Text("[pwd-brkr] # ", style="green")
    prompt.stylize("white", 11, 13)

    print(
        boxen(
            """
[green]
                ██████╗>██╗>>>>██╗██████╗>>>>>>>██████╗>██████╗>██╗>>██╗██████╗>
                ██╔══██╗██║>>>>██║██╔══██╗>>>>>>██╔══██╗██╔══██╗██║>██╔╝██╔══██╗
                ██████╔╝██║>█╗>██║██║>>██║█████╗██████╔╝██████╔╝█████╔╝>██████╔╝
                ██╔═══╝>██║███╗██║██║>>██║╚════╝██╔══██╗██╔══██╗██╔═██╗>██╔══██╗
                ██║>>>>>╚███╔███╔╝██████╔╝>>>>>>██████╔╝██║>>██║██║>>██╗██║>>██║
                ╚═╝>>>>>>╚══╝╚══╝>╚═════╝>>>>>>>╚═════╝>╚═╝>>╚═╝╚═╝>>╚═╝╚═╝>>╚═╝
                                pwd-brkr v0.2 - dev.release

        pwd-brkr is a clean stringset (basically password) guessing machine that's highly customizable and is aesthetically beautiful. developer version.
[/green]
""",
            style="double",
            text_alignment="center",
            color="green",
        )
    )
    rprint("[yellow]For help in commands, use the '--help' or '-h' flag. Use 'exit' to exit the REPL. Type 'list' for a list of all available commands.[/yellow]\n")
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
