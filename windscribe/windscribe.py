
import os
import random
import re

import attr
from loguru import logger
import pexpect


def remove_ansi_sequences(text):

    return re \
        .compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]') \
        .sub('', text)

def proc_output(child):

    return '\n'.join([
        line.decode() for line in child.readlines()
    ])

@attr.s
class WindscribeLocation:

    name   = attr.ib(type=str)
    abbrev = attr.ib(type=str)
    city   = attr.ib(type=str)
    label  = attr.ib(type=str)

    def __attrs_post_init__(self):

        self.name = remove_ansi_sequences(self.name)
        self.abbrev = remove_ansi_sequences(self.abbrev)
        self.city = remove_ansi_sequences(self.city)
        self.label = remove_ansi_sequences(self.label)

def split_cmd_output(line):

    return [
        output_segment.strip()
        for output_segment in filter(None, line.split('  '))
    ]

def validate_location_headers(headers):

    location_schema = split_cmd_output(headers)

    formatted_attr_names = [
        field.strip().lower().replace(' ', '_')
        for field in location_schema
    ]

    assert formatted_attr_names == [ 'location', 'short_name', 'city_name', 'label' ]

def locations():

    child = pexpect.spawn('windscribe locations')

    headers = remove_ansi_sequences(child.readline().decode())

    validate_location_headers(headers)

    return [
        WindscribeLocation(*split_cmd_output(location.decode()))
        for location in child.readlines()
    ]

def connect(location='best', rand=False):

    if rand:

        location = random.choice(locations())

        location = location.label

    if not rand and isinstance(location, WindscribeLocation):

        location = location.label

    location = location.replace(' ', '\\ ')

    child = pexpect.spawn(f'windscribe connect {location}')

    logger.info(proc_output(child))

def account():

    child = pexpect.spawn('windscribe account')

    logger.info(proc_output(child))
    
def login(user=None, pw=None):

    user = ( user if user 
             else os.environ.get('WINDSCRIBE_USER') ) + "\n"

    pw =  ( pw if pw 
            else os.environ.get('WINDSCRIBE_PW') ) + "\n"

    child = pexpect.spawn('windscribe login')
    logged_in = child.expect([ 'Windscribe Username:', 'Already Logged in' ])

    if logged_in == 0:

        child.sendline(user)
        child.expect('Windscribe Password:')
        child.sendline(pw)

        logger.info(proc_output(child))

        child.terminate()

        return

    if logged_in == 1: 

        logger.info('Already logged in')

        child.terminate()

        return


    raise RuntimeError('Unexpected command line ouput. This library sucks.')

def logout():

    child = pexpect.spawn('windscribe logout')

    logger.info(proc_output(child))

    