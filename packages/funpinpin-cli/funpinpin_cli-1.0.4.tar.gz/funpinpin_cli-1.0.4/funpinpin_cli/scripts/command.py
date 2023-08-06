"""Commans registration."""
import click

from .help import help
from .login import login
from .logout import logout
from .store import store
from .switch import switch
from .version import version
from .populate import (products, customers, draftorders)
from .whoami import whoami

_ansi_reset_all = "\033[0m"
_ansi_color_bright_cyan = "\033[96m"
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    """
    \b
    Use \033[96mfunpinpin <command> --help\033[0m to display detailed information about a specific command.
    \b
    \033[96mlogin\033[0m: Log in to the Funpinpin CLI by authenticating with a store or partner organization
      Usage: \033[96mfunpinpin login [--store STORE]\033[0m
    \b
    \033[96mlogout\033[0m: Log out of an authenticated partner organization and store, or clear invalid credentials
      Usage: \033[96mfunpinpin logout\033[0m
    \b
    \033[96mstore\033[0m: Display current store.
      Usage: \033[96mfunpinpin store\033[0m
    \b
    \033[96mpopulate\033[0m: Populate a Shopify store with example customers, orders, or products.
      Usage: \033[96mfunpinpin populate [ customers | draftorders | products ]\033[0m
    \b
    \033[96mswitch\033[0m: Switch between development stores in your partner organization
      Usage: \033[96mfunpinpin switch [--store STORE]\033[0m
    \b
    \033[96mversion\033[0m: Prints version number.
      Usage: \033[96mfunpinpin version\033[0m
    \b
    \033[96mwhoami\033[0m: Identifies which partner organization or store you are currently logged into.
      Usage: \033[96mfunpinpin whoami\033[0m
    """
    pass


def register_command():
    """Rerister single command."""
    cli.add_command(help)
    cli.add_command(login)
    cli.add_command(logout)
    cli.add_command(store)
    cli.add_command(switch)
    cli.add_command(version)
    cli.add_command(whoami)


@cli.group()
def populate():
    """
    \b
    \033[96mpopulates\033[0m: Populate a Funpinpin store with example customers, orders, or products.
      Usage: \033[96mfunpinpin populate [ customers | draftorders | products ]\033[0m

    Subcommands:

      \b
      \033[96mcustomers [options]\033[0m: Add dummy customers to the specified store.
        Usage: \033[96mfunpinpin populate customers\033[0m

      \b
      \033[96mdraftorders [options]\033[0m: Add dummy orders to the specified store.
        Usage: \033[96mfunpinpin populate draftorders\033[0m

      \b
      \033[96mproducts [options]\033[0m: Add dummy products to the specified store.
        Usage: \033[96mfunpinpin populate products\033[0m

    Options:\n
      \b
      \033[96m--count [integer]\033[0m: The number of dummy items to populate. Defaults to 5.
      \033[96m--silent\033[0m: Silence the populate output.
      \033[96m--help\033[0m: Display more options specific to each subcommand.

    Examples:

      \b
      \033[96mfunpinpin populate products\033[0m
        Populate your store with 5 additional products.

      \b
      \033[96mfunpinpin populate customers --count 30\033[0m
        Populate your store with 30 additional customers.

      \b
      \033[96mfunpinpin populate draftorders\033[0m
        Populate your store with 5 additional orders.

      \b
      \033[96mfunpinpin populate products --help\033[0m
        Display the list of options available to customize the \033[96mfunpinpin populate products\033[0m command.
    """
    pass


def register_populate():
    """Register populate subcommand."""
    populate.add_command(products)
    populate.add_command(customers)
    populate.add_command(draftorders)


register_command()
register_populate()
