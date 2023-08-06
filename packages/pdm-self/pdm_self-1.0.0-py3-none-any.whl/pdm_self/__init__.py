from typing import List

from pdm_self.cli import main as register_plugin

main = register_plugin

__all__: List[str] = ["main"]
