import select
import socket
import struct
from socketserver import StreamRequestHandler, ThreadingTCPServer
SOCKS_VERSION = 5
class SocksProxy(StreamRequestHandler):
    def handle(self):
        print('Accepting connection from {}'.format(self.client_address))
        header = self.connection.recv(2)
        version, nmethods = struct.unpack("!BB", header)
        assert version == SOCKS_VERSION
        assert nmethods > 0
        methods = self.get_available_methods(nmethods)
        if 0 not in set(methods):
            self.server.close_request(self.request)
            return
        self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 0))
        # ÇëÇó
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))
        assert version == SOCKS_VERSION
        if address_type == 1:  # IPv4
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:  # Domain name
            domain_length = self.connection.recv(1)[0]
            address = self.connection.recv(domain_length)
            #address = socket.gethostbyname(address.decode("UTF-8"))
        elif address_type == 4: # IPv6
            addr_ip = self.connection.recv(16)
            address = socket.inet_ntop(socket.AF_INET6, addr_ip)
        else:
            self.server.close_request(self.request)
            return
        port = struct.unpack('!H', self.connection.recv(2))[0]
        try:
            if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                print('Connected to {} {}'.format(address, port))
            else:
                self.server.close_request(self.request)
            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            #reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type, addr, port)
            # ×¢Òâ£º°´ÕÕ±ê×¼Ð­Òé£¬·µ»ØµÄÓ¦¸ÃÊÇ¶ÔÓ¦µÄaddress_type£¬µ«ÊÇÊµ¼Ê²âÊÔ·¢ÏÖ£¬µ±address_type=3£¬Ò²¾ÍÊÇËµÊÇÓòÃûÀàÐÍÊ±£¬»á³öÏÖ¿¨ËÀÇé¿ö£¬µ«ÊÇ½«address_type¸ÃÎª1£¬Ôò²»¹ÜÊÇIPÀàÐÍºÍÓòÃûÀàÐÍ¶¼ÄÜÕý³£ÔËÐÐ
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, 1, addr, port)
        except Exception as err:
            print(str(err))
            reply = self.generate_failed_reply(address_type, 5)
        self.connection.sendall(reply)
        if reply[1] == 0 and cmd == 1:
            self.exchange_loop(self.connection, remote)
        self.server.close_request(self.request)
    def get_available_methods(self, n):
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods
    def generate_failed_reply(self, address_type, error_number):
        return struct.pack("!BBBBIH", SOCKS_VERSION, error_number, 0, address_type, 0, 0)
    def exchange_loop(self, client, remote):
        while True:
            r, w, e = select.select([client, remote], [], [])
            if client in r:
                data = client.recv(4096)
                if remote.send(data) <= 0:
                    break
            if remote in r:
                data = remote.recv(4096)
                if client.send(data) <= 0:
                    break
if __name__ == '__main__':
    server =  ThreadingTCPServer(('0.0.0.0', 9210), SocksProxy)
    print("start server")
    server.serve_forever()
