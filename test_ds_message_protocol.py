import ds_protocol
import json
import unittest

# Sending of direct message was successful
r1 = '{"response": {"type": "ok", "message": "Direct message sent"}}'

# Response to request for **`all`** and **`new`** messages. Timestamp is time in seconds 
# of when the message was originally sent.
r2 = '{"response": {"type": "ok", "messages": [{"message":"Hello User 1!", "from":"markb", "timestamp":"1603167689.3928561"},{"message":"Bzzzzz", "from":"thebeemoviescript", "timestamp":"1603167689.3928561"}]}}'

print(ds_protocol.extract_dm(r1))

print(ds_protocol.extract_dm(r2))

#r3 = json.loads(r2)

class test_protocol(unittest.TestCase):
    def test_join(self):
        m = ds_protocol.join('brian', 'cress')
        assert m == '{"join": {"username": "brian","password": "cress","token":""}}'

    def test_dm_send(self):
        m = ds_protocol.dm_send('message', 'recipient', '10', '101')
        assert m == '{"token":"10", "directmessage": {"entry": "message","recipient":"recipient", "timestamp": "101"}}'
    
    def test_unread(self):
        m = ds_protocol.unread('10')
        assert m == '{"token":"10", "directmessage": "new"}'
    
    def test_unread_all(self):
        m = ds_protocol.unread_all('10')
        assert m == '{"token":"10", "directmessage": "all"}'
    
    def test_extract_json(self):
        m = ds_protocol.extract_json('{"response": {"type": "ok", "message": "", "token":"12345678-1234-1234-1234-123456789abc"}}')
    
    def test_fail_ej(self):
        f = ds_protocol.extract_json('brotha')
        assert f is False

    def test_extract_dm(self):
        m = ds_protocol.extract_dm('{"response": {"type": "ok", "message": "Direct message sent"}}')
        assert m == {"type": "ok", "message": "Direct message sent"}
    
    def test_extract_dm_fail(self):
        m = ds_protocol.extract_dm('bruh')
        assert m is False
