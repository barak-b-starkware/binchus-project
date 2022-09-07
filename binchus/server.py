import sys
import threading
from pathlib import Path
from . import CommandLineInterface
from .utils.listener import Listener
from . import Thought

cli = CommandLineInterface()


class Handler(threading.Thread):
    def __init__(self, client, data_dir, lock):
        super().__init__()
        self.client = client
        self.data_dir_path = Path(data_dir)
        self.lock = lock
        self.msg = None
        self.thought = None

    def run(self):
        msg = self.read_message()
        if len(msg) < 20:
            raise Exception("Incomplete meta data received.")
        self.thought = Thought.deserialize(msg)
        self.lock.acquire()
        self.write_thought()
        self.lock.release()
        self.client.stop()

    def read_message(self):
        msg = bytearray(self.client.receive(1024))
        while (cont_msg := self.client.receive(1024)):
            msg += cont_msg
        return msg

    def validate_message(self):
        if len(self.msg) < 20:
            raise Exception("Incomplete meta data received.")

    def write_thought(self):
        dir_path = self.data_dir_path / f'{self.thought.user_id}'
        dir_path.mkdir(parents=True, exist_ok=True)
        file_path = \
            dir_path / f'{self.thought.timestamp:%Y-%m-%d_%H-%M-%S}.txt'
        file_path.touch()
        with file_path.open(mode='r+') as f:
            if f.read() == '':
                f.write(f'{self.thought.thought}')
            else:
                f.write(f'\n{self.thought.thought}')


@cli.command
def run_server(address, data):
    ip, port = address.split(":", 1)
    with Listener(port=int(port), host=ip) as listener:
        lock = threading.Lock()
        while True:
            client = listener.accept()
            newthread = Handler(client, data, lock)
            newthread.start()
    # listener = Listener(port=int(port), host=ip)                ###
    # server = socket.socket()
    # server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # server.bind((ip, int(port)))
    # listener.start()                                            ###
    # server.listen(1000)
    # lock = threading.Lock()                                     ###
    # while True:                                                 ###
    #    client = listener.accept()                               ###
    #    newthread = Handler(client, data, lock)                  ###
    #    newthread.start()                                        ###


def main(argv):
    if len(argv) != 3:
        print(f'USAGE: {argv[0]} <address> <data_dir>')
        return 1
    try:
        run_server(sys.argv[1], sys.argv[2])
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(cli.main())
