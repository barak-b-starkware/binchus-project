Binchus-Project API Reference
=============================

This is Binchus-Project's API reference.

Client
______

.. method:: upload_thought(address, user_id, thought)

    Upload thought of some user to the given address.

Server
______

.. class:: server.Handler(client, data_dir, lock)

    An handler that inherits from threading.Thread and serves as handler to accept connections on the server.

    .. method:: __init__(self, client, data_dir, lock)

        A constructor.
    
    .. method:: run(self)

        Reads the message, validates it, deserializes the given thought and finally writes it (uses the lock when writing).

.. method:: run_server(address, data_dir)

    Runs a server on the given address serving the given directory.

Thought
_______

.. class:: thought.Thought(user_id, timestamp, thought)

    A thought object.

    .. method:: serialize(self)

        Serializes the thought in the following way: user_id -> 8 bytes, timestamp -> 8 bytes, length in bytes of the thought -> 4 bytes, thought -> number of required bytes.
        