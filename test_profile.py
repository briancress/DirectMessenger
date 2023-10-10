import unittest
import Profile
import os


class test_profile(unittest.TestCase):
    def test_sent(self):
        s = Profile.SentMessage()
        s.set_message('message')
        s.set_to('to')
        s.set_time(10.0)

    def test_message(self):
        s = Profile.Message()
        s.set_message('message')
        s.set_sender('to')
        s.set_time(10.0)
    
    def test_post(self):
        s = Profile.Post()
        s.set_entry('entry')
        s.get_entry()
        s.set_time(10.0)
        s.get_time()
    
    def test_prof(self):
        path = os.path.abspath('test_profile.dsu')
        post = Profile.Post()
        post.set_entry('entry')
        post.set_time(10.0)
        s = Profile.Profile()
        s.save_profile(path)
        s.add_post(post)
        s.add_message('message')
        s.add_sent_message('sent message')
        s.add_friend('friend')
        s.del_post(0)
        s.get_posts()
        s.get_friends()
        path = os.path.abspath('test_profile.dsu')
        s.load_profile(path)