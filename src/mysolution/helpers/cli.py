from __future__ import annotations

import contextlib
import sys

import click


def command_with_input_file(func):
    """Inserts input file argument to a click's command.
    """
    arg = click.argument(
        'input_file', default='-',
        type=click.Path(exists=True, dir_okay=False, allow_dash=True),
    )
    return click.command(arg(func))


def open_input_file(file):
    """Opens the file using built-in `open()` function if the file is provided.
    Otherwise, it returns the standard input as a fallback (e.g. if the file is a dash).
    The returned value is to be used inside with-context.
    """
    if not file or file == '-':
        return contextlib.nullcontext(sys.stdin)
    return open(file)

