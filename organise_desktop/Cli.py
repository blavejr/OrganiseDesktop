from organiseDesktop import organise_desktop
from organiseDesktop import undo
from cronController import schedule_start, schedule_end
import os
import sys
import json
import click

pwd = os.path.dirname(os.path.abspath(__file__))

Extensions = json.load(open(pwd+'/Extension.json'))

folders = [x for x in Extensions]

@click.command()
@click.option(
    "--undosched",
    "-u",
    is_flag=True,
    help="Undo changes that were made.",
)
@click.option(
    "--sched",
    "-s",
    is_flag=True,
    help="Schedule an organization process to run."
)
@click.option(
    "--desched",
    "-d",
    is_flag=True,
    help="Remove a scheduled organization process."
)
@click.option(
    "--ignore",
    "-i",
    type=str,
    multiple=True,
    help="Identify which file extension to exclude from organization. This should be passed for each file extension."
)
def cli(
    undosched,
    sched,
    desched,
    ignore
):
    """
    This is used to call a command line interface.
    """
    if undosched:
        undo()

    elif sched:
        schedule_start(folders)

    elif desched:
        schedule_end()

    elif ignore:

        tmp_ext_list = []
        for i in ignore: # Create a tuple with all the given extensions
            tmp_ext_list.extend(i.split(','))

        extension_tuple = tuple([ # add periods to the start of extensions if not already there
            x if x[0] == '.' else f".{x}" for x in tmp_ext_list
        ])

        to_clean = { # create a dict that doesn't include the provided extensions, based on the extensions in the json file
            category: [
                extension for extension in Extensions[category] if extension not in extension_tuple
            ] for category in Extensions
        }

        organise_desktop(to_clean)

    else:
        organise_desktop(Extensions)

    sys.exit()

if __name__ == '__main__':
    cli()
