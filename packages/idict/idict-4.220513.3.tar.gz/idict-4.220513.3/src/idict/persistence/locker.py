#  Copyright (c) 2022. Davi Pereira dos Santos
#  This file is part of the i-dict project.
#  Please respect the license - more about this in the section (*) below.
#
#  i-dict is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  i-dict is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with i-dict.  If not, see <http://www.gnu.org/licenses/>.
#
#  (*) Removing authorship by any means, e.g. by distribution of derived
#  works or verbatim, obfuscated, compiled or rewritten versions of any
#  part of this work is illegal and it is unethical regarding the effort and
#  time spent here.
#

import shelve
from contextlib import contextmanager
from datetime import datetime, timedelta

from temporenc import packb, unpackb


def locker(iterable, dict_shelf=None, timeout=None, logstep=1):
    """
    Generator that skips items from 'iterable' already processed before or still being processed

    Item processing is restarted if 'timeout' expires.
    'dict_shelf' is a dict-like or a shelve-like object to store each item status
        when 'None', 'shelve.open("/tmp/locker.db")' will be used
    'logstep' is the frequency of printed messages, 'None' means 'no logs'.
    'timeout'=None keeps the job status as 'started' forever (or until it finishes)

    >>> from time import sleep
    >>> names = ["a","b","c","d","e"]
    >>> storage = {}
    >>> for name in locker(names, dict_shelf=storage, timeout=10):
    ...    print(f"Processing {name}")
    ...    sleep(0.1)
    ...    print(f"{name} processed!")
    'a' is new, started
    Processing a
    a processed!
    'a' done
    'b' is new, started
    Processing b
    b processed!
    'b' done
    'c' is new, started
    Processing c
    c processed!
    'c' done
    'd' is new, started
    Processing d
    d processed!
    'd' done
    'e' is new, started
    Processing e
    e processed!
    'e' done
    >>> storage
    {'a': b'd', 'b': b'd', 'c': b'd', 'd': b'd', 'e': b'd'}
    >>> for name in locker(names, dict_shelf=storage, timeout=10):
    ...    print(f"Processing {name}")
    ...    sleep(0.1)
    ...    print(f"{name} processed!")
    'a' already done, skipping
    'b' already done, skipping
    'c' already done, skipping
    'd' already done, skipping
    'e' already done, skipping
    """
    if dict_shelf is None:
        contextm = shelve.open("/tmp/locker.db")
    elif hasattr(dict_shelf, "__contains__"):
        @contextmanager
        def ctx():
            yield dict_shelf

        contextm = ctx()
    else:
        contextm = dict_shelf

    with contextm as dic:
        for c, item in enumerate(iterable):
            if item in dic:
                val = dic[item]
                if val == b'd':
                    status, action = 'already done', "skipping"
                elif timeout is not None and datetime.now() > unpackb(val).datetime() + timedelta(seconds=timeout):
                    status, action = "expired", "restarted"
                else:
                    status, action = 'already started', "skipping"
            else:
                status, action = "is new", "started"
            if logstep is not None and c % logstep == 0:
                print(f"'{item}' {status}, {action}")
            if action != "skipping":
                dic[item] = packb(datetime.now())
                yield item
                dic[item] = b'd'
                if logstep is not None and c % logstep == 0:
                    print(f"'{item}' done")
