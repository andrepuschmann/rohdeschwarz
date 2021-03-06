import socket

"""
@class rohdeschwarz.bus.tcp.TcpBus
TcpBus provides a VISA-like interface for an instrument
connection using TCP sockets.

Example:
    address = '192.168.35.5'
    port    =  5025

    bus = TcpBus()
    bus.open(address, port)

    # Optional parameters
    # These are the default values:
    bus.buffer_size = 1024
    bus.delimiter = '\n'

    # Read/write strings
    # (delimiter is sent)
    bus.write('*IDN?')
    print('ID: ' + bus.read())

    # Read/write binary data
    # (delimiter not used)
    bus.write(b'#3256...')

"""

class TcpBus(object):
    """
    TcpBus provides a VISA-like interface for an instrument
    connection using TCP sockets.

    Example:
        address = '192.168.35.5'
        port    =  5025

        TcpBus bus()
        bus.open(address, port)

        # Optional parameters
        # These are the default values:
        bus.buffer_size = 1024
        bus.delimiter = '\n'

        # Read/write strings
        # (delimiter is sent)
        bus.write('*IDN?')
        print('ID: ' + bus.read())

        # Read/write binary data
        # (delimiter not used)
        bus.write(b'#3256...')

    """

    def __init__(self):
        """
        Initialize new TcpBus.
        """
        self.buffer_size = 1024
        self.delimiter = '\n' # Writes
        self._socket = None

    def __del__(self):
        if self._socket:
            self.close()

    def open(self, address='127.0.0.1', port=5025):
        """
        Open TCP socket connection.

        Args:
            address (str): address of instrument
            port (int): TCP port of instrument

        Raises:
            socket.timeout: if instrument not found

        """
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.timeout_ms = 1000
        self._socket.connect((address, port))

    def close(self):
        """
        Close connection
        """
        self._socket.close()
        self._socket = None

    def read(self):
        """
        Read until delimter is received

        Returns:
            str: read string

        Raises:
            socket.timeout: if instrument not found
        """
        result = self._socket.recv(self.buffer_size).decode()
        while not result.endswith(self.delimiter):
            result += self._socket.recv(self.buffer_size).decode()
        return result

    def write(self, buffer):
        """
        Write 'buffer' + delimiter

        Args:
            buffer (str): string to write

        Raises:
            socket.timeout: if instrument not found
        """
        if isinstance(buffer, str):
            buffer = buffer.encode()
        self.write_raw_no_end(buffer + self.delimiter.encode())

    def read_raw_no_end(self, buffer_size=1024):
        """
        Read up to 'buffer_size' bytes

        Args:
            buffer_size (int): buffer size in bytes

        Returns:
            bytes (b'...'): read result


        Raises:
            socket.timeout: If instrument not found
        """
        return self._socket.recv(buffer_size)

    def write_raw_no_end(self, buffer):
        """
        Write 'buffer' without delimiter

        Args:
            buffer (bytes): Raw data to write

        Raises:
            socket.timeout: if instrument not found
        """
        if not isinstance(buffer, bytes):
            buffer = bytes(buffer, 'utf-8')
        self._socket.sendall(buffer)

    def _timeout_ms(self):
        """
        Timeout

        Args:
            timeout (int): milliseconds

        Returns:
            timeout (int): milliseconds
        """
        if not self._socket.gettimeout():
            return 0
        return self._socket.gettimeout() * 1000
    def _set_timeout_ms(self, value):
        self._socket.settimeout(value/1000)
    timeout_ms = property(_timeout_ms, _set_timeout_ms)


    def status_string(self):
        """
        Included for compatibility purposes

        Returns:
            None
        """
        return None
