#!/usr/bin/python
import re

re.match(r'^\d{3}\-\d{3-8}$','010-12345')

#[0-9a-zA-Z\_]
#[0-9a-zA-Z\_]+
#[a-zA-Z\_][0-9a-zA-Z\_]*
#[a-zA-Z\_][0-9a-zA-Z\_]{0, 19}
#[P|p]ython]
#\d$
