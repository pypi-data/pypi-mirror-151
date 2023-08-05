# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Copyright:   (c) 2021 ff. Michael Amrhein (michael@adrhinum.de)
# License:     This program is part of a larger application. For license
#              details please read the file LICENSE.TXT provided together
#              with the application.
# ----------------------------------------------------------------------------
# $Source: run_doctests.py $
# $Revision: 2021-06-03T16:37:04+02:00 $


"""Doc tests runner"""

import doctest
import importlib
import sys

flags = doctest.NORMALIZE_WHITESPACE | doctest.IGNORE_EXCEPTION_DETAIL
mod_name = sys.argv[1]
mod = importlib.import_module(mod_name)

print(f"Testing {mod}:")
fail, total = doctest.testmod(mod, optionflags=flags)
print(f"{total} tests, {fail} failures")

sys.exit(fail > 0)
