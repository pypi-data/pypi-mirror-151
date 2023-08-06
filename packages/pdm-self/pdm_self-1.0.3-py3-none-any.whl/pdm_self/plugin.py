import subprocess
import os

from pdm.cli.commands.base import BaseCommand


class SelfCommand(BaseCommand):
    """ """

    def add_arguments(self, parser):
        parser.add_argument("update", default=None, help="")

    def handle(self, project, options):
        if options.update:
            home_dir = os.getenv("HOME")
            update_cmd = (
                f"{home_dir}/.local/share/pdm/venv/bin/python -m pip install -U pdm"
            )
            subprocess.run(update_cmd, capture_output=True, text=True).stdout
