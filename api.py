try:
    import simplejson
except:
    import json as simplejson

from subprocess import *
import os

PHP = 'php' # the php command line program
CLI_PHP = os.path.join(os.path.dirname(__file__), 'cli.php')

def oi_services():
    """
    # returns the dict:
    {
        'email': service_dict,
        'social': service_dict
    }
    # where service_dict holds more entries of the form:
        u'twitter': {
            u'base_version': u'1.6.7',
            u'check_url': u'http://twitter.com',
            u'description': u'Get the contacts from a Twitter account',
            u'name': u'Twitter',
            u'type': u'social',
            u'version': u'1.0.6'
        }

    """
    try:
        output = Popen([PHP, CLI_PHP, '--', '--services'], stdout=PIPE).communicate()[0]
        return simplejson.loads(output)
    except Exception, e:
        print e
    

def oi_get_contacts(email, password, provider):
    """
    # returns a dict of the form:

    {u'contacts':   {u'a@yahoo.com': u'afirstname alastname',
                     u'b@yahoo.com': u'bfirstname blastname'},
     u'errors': [],
     u'oi_session_id': u'1238456503.6221'}

    # if there are any errors, there will be a dict (see cli.php for the keys) in the place of that empty list
    """
    try:
        output = Popen([PHP, CLI_PHP, '--', '--contacts', email, password, provider], stdout=PIPE).communicate()[0]
        return simplejson.loads(output)
    except Exception, e:
        print e
    
def oi_send_message(subject, body, provider, contacts, email, password):
    """
    contacts - needs to be a list
    # returns:
        {'result': res, 'errors': []}
    # if the result is False, there was an error; if it's -1 the plugin can't handle sending messages
    """
    try:
        output = Popen([PHP, CLI_PHP, '--', '--send-message', subject, body, provider, simplejson.dumps(contacts), email, password], stdout=PIPE).communicate()[0]
        return simplejson.loads(output)
    except Exception, e:
        print e

