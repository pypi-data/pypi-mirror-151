#!/usr/bin/python

import sys, getopt
from . import constants
from .prints import Prints
from .translator import Translator
from .configuration import Configuration

prints = Prints()
translator = Translator()
configuration = Configuration()


def exit_app( value = 0 ):
    sys.exit( value )


def helper():

    print( f'Usage: { constants.APP } [OPTIONS]\n' )
    print(f"{'Option' : <30}Explanation")
    print(f"{'--------' : <30}-------")
    for argument in constants.ARGUMENTS:
        arguments = f'{ argument.get_short() }, { argument.get_long() }'
        print(f"{ arguments : <30}{argument.message}")

    exit_app()


def set_vars_from_args(argv):
    help = constants.ARGUMENTS[0]
    message = constants.ARGUMENTS[1]
    first = constants.ARGUMENTS[2]
    second = constants.ARGUMENTS[3]

    try:
        opts, args = getopt.getopt(argv,
        f"{ help.short }{ message.short }:{ first.short }:{ second.short }:",
        [ help.long, f"{ message.long }=", f"{ first.long }=", f"{ second.long }=" ])

    except getopt.GetoptError:
        exit_app( 2 )

    for opt, arg in opts:
        if opt in help.get_full():
            helper()
        elif opt in message.get_full():
            message.set_value( arg )
        elif opt in first.get_full():
            first.set_value( arg )
        elif opt in second.get_full():
            second.set_value( arg )


def checkFunction( text ):

    if ( text == constants.EXIT ):
        exit_app()
    elif ( text == constants.CLEAR ):
        prints.clear()
        return True
    
    return False


def main():
    argument = sys.argv[1:]
    set_vars_from_args(argument)
    configuration.check_languages()

    if ( not argument ):
        prints.print_informations()
        translator.translation_loop()
    else:
        message = constants.ARGUMENTS[1]
        translator.translate( message.value )
