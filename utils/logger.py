import os
from datetime import datetime
from rich.console import Console

console = Console(soft_wrap=True,
                  highlight=False)

def info(msg: str):
    console.print(f"[sky_blue2]{datetime.now().strftime("%X")} | info[/sky_blue2]: {msg}")
def success(msg: str):
    console.print(f"[honeydew2]{datetime.now().strftime("%X")} | success[/honeydew2]: {msg}")
def warn(msg: str):
    console.print(f"[light_goldenrod2]{datetime.now().strftime("%X")} | warning[/light_goldenrod2]: {msg}")
def err(msg: str):
    console.print(f"[deep_pink2]{datetime.now().strftime("%X")} | error[/deep_pink2]: {msg}")
def verbose(msg: str):
    if "RITSU_DEBUG" in os.environ:
        console.print(f"[light_cyan1]{datetime.now().strftime("%X")} | verbose[/light_cyan1]: {msg}")