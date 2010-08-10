#!/usr/bin/env python

# normally you would have pyopeninviter in your python path and won't need to do this injection
import sys
sys.path.insert(0, '..')

from pyopeninviter.api import *
from pprint import pprint

TEST_PROVIDER = 'gmail'
TEST_ACCOUNT = 'someuser@gmail.com'
TEST_PWD = 'somepassword'

services = oi_services()
pprint(services['email']['gmail'])

contacts = oi_get_contacts(TEST_ACCOUNT, TEST_PWD, TEST_PROVIDER)
pprint(contacts['contacts'])

# the 'gmail' plugin can't send messages. try with a twitter account
#output = oi_send_message('testing', '1, 2, 3... testing', TEST_PROVIDER, contacts['contacts'].keys(), TEST_ACCOUNT, TEST_PWD)
#pprint(output)

