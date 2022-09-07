import sys
# from . import run_server, upload_thought
from . import run_webserver, CommandLineInterface

cli = CommandLineInterface()

if __name__ == '__main__':
    cli.command(run_webserver)
    sys.exit(cli.main())
