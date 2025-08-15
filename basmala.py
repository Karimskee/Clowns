import pyfiglet
from colorama import Fore, Style, init
init(autoreset=True)

# check name has first and last
banner = pyfiglet.figlet_format("Basmala",font="block")
print(Fore.CYAN + Style.BRIGHT+ banner)
