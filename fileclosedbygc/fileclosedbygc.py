# -*- coding: utf-8 -*-

"""Main module."""

import __builtin__
import logging
import os
import traceback


log = logging.getLogger('fileclosedbygc')

modes_to_filter = os.environ.get('CLOSEDBYGC', 'r,rb').split(',')


def stack():
    setattr(__builtin__, 'open', orig_open)
    result = traceback.format_stack()
    setattr(__builtin__, 'open', trace_open)
    return result


class TracedFile(file):

    def __init__(self, *args, **kwargs):
        super(TracedFile, self).__init__(*args, **kwargs)
        self.open_stack = stack()

    def close(self):
        log.debug("Closed %s", self.name)
        super(TracedFile, self).close()

    def __new__(typ, name, mode):
        log.debug("New TracedFile %s %s", name, mode)
        new = file.__new__(typ, name, mode)
        return new

    def __del__(self):
        if not self.closed and self.mode not in modes_to_filter:
            self.log_stack()
            self.close()

    def log_stack(self):
        tolog = list()
        tolog.append("Closed by GC %s" % self.name)
        tolog.extend(stack()[:-3])
        tolog.append("Opened at")
        tolog.extend(self.open_stack[:-3])
        log.info('\n'.join(tolog))


def trace_open(name, mode='r'):
    log.debug("Open %s", name)
    return TracedFile(name, mode)

orig_open = __builtin__.open
setattr(__builtin__, 'open', trace_open)
log.warning('Monkeypatching builtin open')
