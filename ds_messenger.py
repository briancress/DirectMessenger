"""Module for interacting with server to send messages"""
import socket
import json
import time
import ds_protocol as dsp


class DirectMessage:
    """Class for message objects"""
    def __init__(self, recipient=None, message=None, timestamp=None):
        """Initialize values"""
        self.recipient = recipient
        self.message = message
        self.timestamp = timestamp


class DirectMessenger:
    """Class for messaging"""
    def __init__(self, dsuserver=None, username=None, password=None):
        """Initialize values"""
        self.token = None
        self.dsuserver = dsuserver
        self.port = 3021
        self.username = username
        self.password = password

    def get_token(self):
        """Gets token to use later"""
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server = self.dsuserver
        port = self.port
        try:
            if not isinstance(self.username, str):
                raise TypeError("Username should be a string")
            if not isinstance(self.password, str):
                raise TypeError("Password should be a string")
            if not isinstance(self.dsuserver, str):
                raise TypeError('Server should be a string')
        except TypeError as e:
            print(f'Error: {e}')
            return False
        try:
            client_socket.connect((server, port))
        except TimeoutError:
            print('Could not connect to server, server timed out')
            return False
        except OverflowError:
            print('Port is invalid')
            return False
        except socket.gaierror:
            print('Address or port is invalid')
            return False
        except ConnectionRefusedError:
            print('Bad Address (not numbers)')
            return False
        except TypeError:
            print('Values are NoneType')
            return False
        except OSError:
            print('No internet')
            return False
        join_data = dsp.join(self.username, self.password)

        try:
            client_socket.sendall(join_data.encode())
            join_received = client_socket.recv(1024).decode()

        except:
            print('Could not send username or password')
            return False

        # EXTRACTION
        try:
            post_extraction = dsp.extract_json(join_received)
        except UnboundLocalError:
            return False

        try:
            if post_extraction.response['type'] == 'ok':
                token = post_extraction.token
                self.token = token
            else:
                return False
        except AttributeError:
            return False

    def send(self, message: str, recipient: str) -> bool:
        """Sends message to other user"""
        # must return true if message successfully sent, false if send failed.
        try:
            if not isinstance(message, str):
                raise TypeError("Message should be a string")
            if not isinstance(self.dsuserver, str):
                raise TypeError('Server should be a string')
            if not isinstance(recipient, str):
                raise TypeError('Recipient should be a string')
        except TypeError as e:
            print(f'Error: {e}')
            return False
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.get_token() is not False:

            client_socket.connect((self.dsuserver, self.port))
            timestamp = str(time.time())
            dm = dsp.dm_send(message, recipient, self.token, timestamp)

            client_socket.sendall(dm.encode())
            dm_received = client_socket.recv(1024).decode()
            dm_result = dsp.extract_dm(dm_received)
            if dm_result['type'] == 'ok':
                return True
            else:
                return False
        else:
            return False

    def retrieve_new(self) -> list:
        """Retrieves new messages from system"""
        # must return a list of DirectMessage objects containing all new messages
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.get_token() is not False:
            server = self.dsuserver
            port = self.port
            client_socket.connect((server, port))
            new_messages = dsp.unread(self.token)

            client_socket.sendall(new_messages.encode())
            new_received = client_socket.recv(1024).decode()

            all_list = []
            new_received = json.loads(new_received)
            fin_messages = new_received['response']['messages']
            for i in fin_messages:
                message = i['message']
                recipient = i['from']
                timestamp = i['timestamp']
                direct_message = DirectMessage(recipient, message, timestamp)
                all_list.append(direct_message)
            return all_list
        else:
            return False

    def retrieve_all(self) -> list:
        """Retrives all messages from server"""
        # must return a list of DirectMessage objects containing all messages
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if self.get_token() is not False:
            server = self.dsuserver
            port = self.port
            client_socket.connect((server, port))
            all_messages = dsp.unread_all(self.token)

            client_socket.sendall(all_messages.encode())
            all_received = client_socket.recv(1024).decode()

            all_list = []
            all_received = json.loads(all_received)
            fin_messages = all_received['response']['messages']

            for i in fin_messages:
                message = i['message']
                recipient = i['from']
                timestamp = i['timestamp']
                direct_message = DirectMessage(recipient, message, timestamp)
                all_list.append(direct_message)

            return all_list
        else:
            return False
