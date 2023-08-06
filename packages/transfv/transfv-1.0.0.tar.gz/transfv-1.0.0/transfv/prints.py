import sys, os
from . import constants

class Prints:

    def print_informations( self ):
        print( "Google translator (googletrans==4.0.0-rc1)" )
        print( 'Type "exit()" for exited this app, and "clear()" for clearing all a texts.' )


    def print_loading( self ):
        sys.stdout.write( constants.LOADING );
        sys.stdout.flush()


    def print_trans( self, text ):
        print( constants.LAST_LINE + text )
    

    def clear_console( self ):
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)

    
    def clear( self ):
        self.clear_console()
        self.print_informations()