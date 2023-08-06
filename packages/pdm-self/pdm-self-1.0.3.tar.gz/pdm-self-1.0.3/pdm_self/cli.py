from pdm.core import Core as _Core

from pdm_self.plugin import SelfCommand as _Command


def main(core: _Core) -> None:
    core.register_command(_Command, "self")
