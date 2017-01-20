# -*- coding: utf-8 -*-
#    Copyright (c) 2017 Feng Shuo
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0

import commands

__all__ = ['NginxReload', ]


class NginxReload(object):

    __slots__ = ('_ngx_rld', 'ngx_rld', '_ngx_chk', 'ngx_chk')

    def __init__(self):
        self._ngx_chk = "nginx -t"
        self._ngx_rld = "nginx -s reload"

    @property
    def ngx_rld(self):
        return self._ngx_rld

    @ngx_rld.setter
    def ngx_rld(self, cmd):
        self._ngx_rld = cmd

    @property
    def ngx_chk(self):
        return self._ngx_chk

    @ngx_chk.setter
    def ngx_chk(self, cmd):
        self._ngx_chk = cmd

    def ngx_reload(self):
        if commands.getstatusoutput(self.ngx_chk)[0] == 0:
            (status, output) = commands.getstatusoutput(self.ngx_rld)
            return status if status == 0 else exit(1)