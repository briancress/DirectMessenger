"""Module for testing ds_messenger"""
import ds_messenger as dm
import Profile
import unittest


class test_ds_messenger(unittest.TestCase):
    """Class for testing"""
    def test_direct_message(self):
        d = dm.DirectMessage('recipient', 'message', 10.0)
    
    def test_direct_messenger(self):
        d = dm.DirectMessenger('168.235.86.101', 'testunittest', 'tbp')
        d.get_token()
        d.send('unittest', 'Goomba')
        d.retrieve_new()
        d.retrieve_all()
    
    def test_fail_bad_address(self):
        d = dm.DirectMessenger('168.235', 'testunittest', 'tbp')
        d.get_token()
    
    def test_fail_nonetype(self):
        d = dm.DirectMessenger()
        d.get_token()

    def test_fail_bad_port(self):
        d = dm.DirectMessenger('168.235.86.101', 'testunittest', 'tbp')
        d.port = 101230122
        d.get_token()
    
    def test_fail_bad_port2(self):
        d = dm.DirectMessenger('stirrup', 'testunittest', 'tbp')
        d.get_token()

    def test_fail_bad_port3(self):
        d = dm.DirectMessenger('168', 'testunittest', 'tbp')
        d.port = 'string'
        d.get_token()