from __future__ import annotations

import re
import sys


def main():
    for path in sys.argv[1:] or sys.stdin.read().splitlines():
        with open(path, 'r') as path_fd:
            for line, text in enumerate(path_fd.readlines()):
                match = re.search(r'(?<! six)\.(itervalues)', text)

                if match:
                    print('%s:%d:%d: use `dict.values` or `ansible.module_utils.six.itervalues` instead of `dict.itervalues`' % (
                        path, line + 1, match.start(1) + 1))


if __name__ == '__main__':
    main()
