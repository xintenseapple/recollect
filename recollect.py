from __future__ import annotations

import argparse
from typing import Generator

import volatility3.framework.interfaces.context as context
import volatility3.framework.interfaces.plugins as plugins
import volatility3.framework.interfaces.renderers as renderers


class ReCollect(plugins.PluginInterface):
    _version = (1, 0, 0)
    _required_framework_version = (2, 0, 0)

    def __init__(self,
                 ctx: context.ContextInterface,
                 config_path: str) -> None:
        super().__init__(ctx, config_path)

    def _generator(self) -> Generator[tuple[int, tuple], None, None]:
        pass

    def run(self) -> renderers.TreeGrid:
        return renderers.TreeGrid([], self._generator())


def main() -> int:
    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        'recollect',
        description='Tool for finding data structures in arbitrary memory dumps. Implemented as a Volatility3 plugin.')

    parser.add_argument()

    main()
