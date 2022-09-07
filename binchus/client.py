import sys
import datetime as dt
from . import CommandLineInterface
from . import Thought
from .utils import Connection

cli = CommandLineInterface()


@cli.command
def upload_thought(address, user, thought):
    ip, port = address.split(":", 1)
    # encoded_thought = thought.encode('utf-8')
    # t = Thought(user, time.time(), encoded_thought)
    t = Thought(user, dt.datetime.now(), thought)
    with Connection.connect(ip, int(port)) as connection:
        connection.send(t.serialize())
    # msg = thought.serialize()
    # conn = socket.socket()
    # conn.connect((ip, int(port)))
    # c = Connection(conn)
    # c.send(msg)
    # c.close()
    print('done')


def main(argv):
    if len(argv) != 4:
        print(f'USAGE: {argv[0]} <address> <user_id> <thought>')
        return 1
    try:
        upload_thought(argv[1], argv[2], argv[3])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(cli.main())
