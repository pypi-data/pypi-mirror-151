import subprocess
import os

from pdm.cli.commands.base import BaseCommand


class SelfCommand(BaseCommand):
    """
    """

    def add_arguments(self, parser):
        parser.add_argument("update", help="")

    def handle(self, project, options):
        if options.update:
            home_dir = os.getenv("HOME")
            update_cmd = f"{home_dir}/.local/share/pdm/venv/bin/python -m pip install -U pdm"
            process = subprocess.Popen(update_cmd.split(), stdout=subprocess.PIPE)
            output, error = process.communicate()
        else:
            print("boop")