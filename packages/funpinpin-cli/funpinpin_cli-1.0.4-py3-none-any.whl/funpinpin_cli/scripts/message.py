"""command message."""
import shutil

import click

from funpinpin_cli.config import DOMAIN_SUFFIX

columns, lines = shutil.get_terminal_size()

ERROR_LEFT_TOP = "┏━━━━ Error "
ERROR_LEFT_FIR = "┃ x "
ERROR_LEFT_MID = "┃ "
ERROR_LEFT_BOT = "┗"

ERROR_TOP = (
    click.style(ERROR_LEFT_TOP, fg="red") +
    click.style("━" * (columns - len(ERROR_LEFT_TOP)), fg="red") +
    "\n"
)
ERROR_FIR = click.style(ERROR_LEFT_FIR, fg="red")
ERROR_MID = click.style(ERROR_LEFT_MID, fg="red")
ERROR_BOT = (
    click.style(ERROR_LEFT_BOT, fg="red") +
    click.style("━" * (columns - len(ERROR_LEFT_BOT)), fg="red")
)

MSG_NO_STORE = (
    ERROR_TOP +
    ERROR_FIR +
    click.style("No store found. Please run", fg="red") +
    " " +
    click.style("funpinpin login --store STORE", fg="bright_cyan") +
    click.style(" to login to a specific store", fg="red") +
    "\n" +
    ERROR_BOT
)

MSG_NO_PARTNER = (
    "It doesn't appear that you're logged in. " +
    "You must log into a partner organization or a store staff account.\n" +
    "\n" +
    "If trying to log into a store staff account, please use " +
    click.style("funpinpin login --store STORE", fg="bright_cyan") +
    " to log in."
)


def get_login_msg(shop, partner_name):
    """Get login shop successfully message."""
    if not shop:
        msg = (
            "Logged into partner organization " +
            click.style(f"{partner_name}", fg="green")
        )
    else:
        msg = (
            "Logged into store " +
            click.style(f"{shop} ", fg="green") +
            "in partner organization " +
            click.style(f"{partner_name}", fg="green")
        )
    return msg


def get_invalid_shop_msg(shop):
    """Get invalid shop message."""
    msg = (
        f"Invalid store provided ({shop}). " +
        "Please provide the store in the following format: " +
        f"my-store.v3.myfunpinpin.{DOMAIN_SUFFIX}"
    )
    msg_formatted = ERROR_TOP
    if (len(msg) + len(ERROR_LEFT_FIR) - columns) <= 0:
        msg_formatted += (
            ERROR_FIR +
            click.style(msg, fg="red") + "\n" +
            ERROR_BOT
        )
    else:
        msg_formatted += (
            ERROR_FIR + click.style(msg[:columns - 4], fg="red") + "\n"
        )
        msg_left = len(msg) - columns + len(ERROR_LEFT_FIR)
        msg_lines = msg_left // (columns - 2)
        j = columns - 4
        for i in range(msg_lines):
            msg_mid = ERROR_MID + click.style(
                msg[j: j + columns - 2] + "\n", fg="red"
            )
            msg_formatted += msg_mid
            j += (columns - 2)
        if j <= len(msg):
            msg_last = ERROR_MID + click.style(
                msg[j:] + "\n", fg="red"
            )
            msg_formatted += msg_last
        msg_formatted += ERROR_BOT
        return msg_formatted

    return msg_formatted


def get_populate_begin_msg(shop):
    """Get message before populate."""
    msg = \
        "Proceeding using " + click.style(f"{shop}", fg="green")
    return msg


def get_populate_msg(shop, obj_type, obj_name, obj_id):
    """Get obj message when created successfully."""
    msg = \
        f"{obj_name} added to " + \
        click.style(f"{shop}", fg="green") + \
        " at " + \
        click.style(
            f"https://{shop}/admin/{obj_type}/{obj_id}",
            underline=True
        )
    return msg


def get_populate_end_msg(shop, obj_type, count):
    """Get message after populate."""
    msg = (
        f"Successfully added {count} {obj_type.capitalize()} to " +
        click.style(f"{shop}\n", fg="green") +
        "View all Products at " +
        click.style(f"https://{shop}/admin/{obj_type}", underline=True)
    )
    return msg


def get_switch_same_strore_msg(shop):
    """Get message when switch to the same store."""
    msg = \
        "Using development store " + \
        click.style(f"{shop}\n", fg="green") + \
        "Switched development store to " + \
        click.style(f"{shop}", fg="green")
    return msg

