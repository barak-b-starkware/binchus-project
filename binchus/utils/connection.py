import socket


class Connection:
    def __init__(self, conn):
        self.conn = conn
        self.ip, self.port = self.conn.getsockname()
        self.peer_ip, self.peer_port = self.conn.getpeername()

    def __repr__(self):
        return f'<Connection from {self.ip}:{self.port} \
                to {self.peer_ip}:{self.peer_port}>'

    def send(self, data):
        self.conn.sendall(data)

    def receive(self, size):
        msg = self.conn.recv(size)
        print(msg)
        if len(msg) < size:
            raise Exception("Connection was closed \
                            before all data was received.")
        return msg

    def close(self):
        self.conn.close()

    def __enter__(self):
        return self

    def __exit__(self, exception, error, traceback):
        self.close()

    def connect(host, port):
        conn = socket.socket()
        conn.connect((host, port))
        return Connection(conn)
