import datetime
from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User

from .domain import Post, Parcel, Hashtag, UserMention, Url, Tweet, format_datetime


class LogicTest(TestCase):
    '''zeitgeist testing'''

    def test_Twitter_to_datetime(self):
        Twitter_datetime_str = 'Wed Apr 26 17:43:16 +0000 2017'
        my_datetime = format_datetime(Twitter_datetime_str)

    def test_build_Post_structures(self):
        my_datetime = format_datetime('Wed Apr 26 17:43:16 +0000 2017')
        my_post = Post('Twitter', 'somename', my_datetime, 'This is what happens when a twit speaks:')
        self.assertEqual(my_post.platform, 'Twitter')
        self.assertEqual('somename', my_post.user_name)
        self.assertEqual(datetime.datetime(2017, 4, 26, 17, 43, 16, tzinfo=datetime.timezone.utc), my_post.post_time)
        self.assertEqual('This is what happens when a twit speaks:', my_post.text)

    def test_build_Parcel_structures(self):
        my_parcel = Parcel('Twitter', 'sometxt')
        self.assertEqual(my_parcel.category, 'Twitter')
        self.assertEqual(my_parcel.text, 'sometxt')

    def test_build_Hashtag_structure(self):
        my_hashtag = Hashtag('hashtag','txtblob')
        self.assertEqual(my_hashtag.__repr__(), '#txtblob')
        self.assertEqual(my_hashtag.text, 'txtblob')
        self.assertEqual(my_hashtag.category, 'hashtag')

    def test_build_UserMention_structure(self):
        my_user_mention = UserMention('user_mention', 'nametxt')
        self.assertEqual(my_user_mention.__repr__(), '@nametxt')
        self.assertEqual(my_user_mention.category, 'user_mention')
        self.assertEqual(my_user_mention.text, 'nametxt')

    def test_build_Url_structure(self):
        my_url = Url('url', 'https://t.co/vKonTficpv')
        self.assertEqual(my_url.__repr__(), 'https://t.co/vKonTficpv')
        self.assertEqual(my_url.text, 'https://t.co/vKonTficpv')
        self.assertEqual(my_url.category, 'url')

    def test_build_Tweet_structure(self):
        some_datetime = format_datetime('Thu Apr 27 15:27:48 +0000 2017')
        my_tweet = Tweet('someguy', some_datetime, 'This guys said some important stuff', False,
                         [Hashtag('Twitter', 'pdxrocks'), Hashtag('Twitter','codeisawesome')],
                         [UserMention('Twitter', 'somedude'), UserMention('Twitter', 'pythongal')],
                         [Url('Twitter', 'https://t.co/Ymtxgvdx2u')])
        self.assertEqual(my_tweet.__repr__(), 'Tweet(04/27/17 15:27:48 UTC, someguy, '
                                              'This guys said some important stuff, False, '
                                              '[#pdxrocks, #codeisawesome], [@somedude, @pythongal], '
                                              '[https://t.co/Ymtxgvdx2u])')



