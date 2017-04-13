"""
Usage:
    Dojo create_room <room_type> <room_name>...
    Dojo add_person <firstname> <lastname> <person_type> [<accommodation>]
    Dojo print_room <room_name>
    Dojo print_allocations [<filename>]
    Dojo print_unallocations [<filename>]
    Dojo print_unallocations [<filename>]
    Dojo (-i | --interactive)
    Dojo (-h | --help)
Options:
    -o, --output  Save to a txt file
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""
import sys, os
import cmd

from docopt import docopt, DocoptExit
from implementation import Implementation


def docopt_cmd(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class MyInteractive (cmd.Cmd):

    prompt = '(Dojo) '
    file = None

    @docopt_cmd
    def do_create_room(self,args):

        """Usage: create_room <room_type> <room_name>..."""
        implementation=Implementation()

        for room_name in args['<room_name>']:
            implementation.create_room(room_name,args['<room_type>'])
            
        
    @docopt_cmd
    def do_add_person(self,args):
        #person.add_person(name,person_type)
        """Usage: add_person <firstname> <lastname> <person_type> [<wants_accomodation>] """
        firstname=args['<firstname>']
        secondname = args['<lastname>']
        person_type = args['<person_type>']
        accommodation_option = args['<wants_accomodation>']

        implementation=Implementation()

        
        implementation.add_person(firstname,secondname,person_type,accommodation_option)

    @docopt_cmd
    def do_print_room(self,args):
        #person.add_person(name,person_type)
        """Usage: print_room <room_name> """
        implementation=Implementation()

        implementation.print_room(args['<room_name>'])

    @docopt_cmd
    def do_print_unallocations(self,args):
        #person.add_person(name,person_type)
        """Usage: print_unallocations [<filename>] """
        implementation=Implementation()
        filename_to_store_allocations=args['<filename>']

        implementation.print_allocations(filename_to_store_allocations)

    @docopt_cmd
    def do_print_allocations(self,args):
        #person.add_person(name,person_type)
        """Usage: print_allocations [<filename>] """
        implementation=Implementation()
        filename_to_store_allocations=args['<filename>']

        implementation.print_allocations(filename_to_store_allocations)

    def do_quit(self, args):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()


opt = docopt(__doc__, sys.argv[1:])
arguments = docopt(__doc__)
#print(arguments)

if opt['--interactive']:
    MyInteractive().cmdloop()
    
print(opt)