# -*- coding: utf-8 -*-
#    Copyright (c) 2017 Feng Shuo
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0

from collections import namedtuple

RequestInfo = namedtuple('RequestInfo', ['IP',          # request ip, type: str
                                         'Datetime',    # request time, type: str
                                         'Path',        # request url/path, type: str
                                         'Status',      # request response code, type: str
                                         'Bandwidth',   # request bandwidth, type: str
                                         'Referrer',    # request referrer, type: str
                                         'Useragent'])  # request user agent, type: str

CrawlerLimit = namedtuple('CrawlerLimit', ['msgs_limit',     # how many msgs do u want to detect, type: int
                                           'rate_limit',     # how many crawlers in certain time&&msgs limit, type: int
                                           'tm_gap_limit'])   # time gap limit in certain msgs/rate condition, type: int
