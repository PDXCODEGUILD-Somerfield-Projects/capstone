import datetime
import json

import re
from django.test import TestCase

from zeitgeist.twitter_data import deserialized_twitter_data, pull_tweet_text, find_most_common_parcels
from .domain import Post, Parcel, Hashtag, UserMention, Url, Tweet, format_datetime

from collections import Counter
from .common_English_words import common_English_words



class LogicTest(TestCase):
    '''zeitgeist testing'''

    def test_Twitter_to_datetime(self):
        Twitter_datetime_str = 'Wed Apr 26 17:43:16 +0000 2017'
        my_datetime = format_datetime(Twitter_datetime_str)


    # testing class structures in zeitgeist:

    def test_build_Post_structures(self):
        my_datetime = format_datetime('Wed Apr 26 17:43:16 +0000 2017')
        my_post = Post('Twitter', 'somename', my_datetime, 'This is what happens when a twit speaks:')
        self.assertEqual(my_post.__repr__(), 'Post(Twitter, 04/26/17 17:43:16 UTC, @somename,'
                                             ' This is what happens when a twit speaks:)')
        self.assertEqual(my_post.platform, 'Twitter')
        self.assertEqual('somename', my_post.user_name)
        self.assertEqual(datetime.datetime(2017, 4, 26, 17, 43, 16, tzinfo=datetime.timezone.utc), my_post.post_time)
        self.assertEqual('This is what happens when a twit speaks:', my_post.raw_text)

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
                         [Url('Twitter', 'https://t.co/Ymtxgvdx2u')], 'This guys said some important stuff')
        self.assertEqual(my_tweet.__repr__(), 'Tweet(04/27/17 15:27:48 UTC, @someguy, '
                                              'This guys said some important stuff, False, '
                                              '[#pdxrocks, #codeisawesome], [@somedude, @pythongal], '
                                              '[https://t.co/Ymtxgvdx2u], This guys said some important stuff)')
        self.assertEqual(my_tweet.platform, 'Twitter')
        self.assertEqual(my_tweet.post_time, datetime.datetime(2017, 4, 27, 15, 27, 48, tzinfo=datetime.timezone.utc))
        self.assertEqual(my_tweet.user_name, 'someguy')
        self.assertEqual(my_tweet.raw_text, 'This guys said some important stuff')
        self.assertEqual(my_tweet.hashtags, [Hashtag('hashtag', 'pdxrocks'), Hashtag('hashtag', 'codeisawesome')])
        self.assertEqual(my_tweet.user_mentions, [UserMention('user_mention', 'somedude'),
                                                  UserMention('Twitter', 'pythongal')])
        self.assertEqual(my_tweet.urls, [Url('Twitter', 'https://t.co/Ymtxgvdx2u')])
        self.assertEqual(my_tweet.clean_text, 'This guys said some important stuff')

    # test Twitter JSON deserialization

    def test_Twitter_JSON_deserialization(self):
        with open('zeitgeist/test_data.json') as source:
            data = json.load(source)
            deserialized = deserialized_twitter_data(data)

        self.assertEqual(deserialized, [Tweet('HeliumComedyPdx', datetime.datetime(2017, 4, 28, 18, 55, 18, tzinfo=datetime.timezone.utc), 'RT @StephKralevich: Our interview with comedy star @tomgreenlive @HeliumComedyPdx .  He talks movies, sausages, Portland &amp; @LeahTiscione ht…', True, [], [UserMention('Twitter', 'StephKralevich'), UserMention('Twitter', 'tomgreenlive'), UserMention('Twitter', 'HeliumComedyPdx'), UserMention('Twitter', 'LeahTiscione')], [], 'Our interview with comedy star . He talks movies, sausages, Portland and ht…'), Tweet('elementaltech', datetime.datetime(2017, 4, 28, 18, 55, 17, tzinfo=datetime.timezone.utc), 'Application Brief: How @AWS @NASA and @elementaltech delivered the first live 4K video from space:… https://t.co/EBqERuI3sF', False, [], [UserMention('Twitter', 'AWS'), UserMention('Twitter', 'NASA'), UserMention('Twitter', 'elementaltech')], [Url('Twitter', 'https://t.co/EBqERuI3sF')], 'Application Brief: How and delivered the first live 4K video from space:… )'), Tweet('LHowlettODPrism', datetime.datetime(2017, 4, 28, 18, 55, 16, tzinfo=datetime.timezone.utc), 'Just b/c you worship the #ProsperityGospel doesn\'t mean you demonize the poor &amp; vulnerable living in the austerity hostel. Don\'t be hostile.', False, [Hashtag('Twitter', 'ProsperityGospel')], [], [], 'Just because you worship the doesn\'t mean you demonize the poor and vulnerable living in the austerity hostel. Don\'t be hostile.')])

        raked_text = pull_tweet_text(deserialized)
        self.assertEqual(raked_text, [('…', 2)])

        test_hashtags = find_most_common_parcels(deserialized, 'hashtags')
        self.assertEqual(test_hashtags, [('ProsperityGospel', 1)])

        test_user_mentions = find_most_common_parcels(deserialized, 'user_mentions')
        self.assertEqual(test_user_mentions, [('StephKralevich', 1), ('tomgreenlive', 1), ('HeliumComedyPdx', 1), ('LeahTiscione', 1), ('AWS', 1), ('NASA', 1), ('elementaltech', 1)])

        test_urls = find_most_common_parcels(deserialized, 'urls')
        self.assertEqual(test_urls, [('https://t.co/EBqERuI3sF', 1)])


def get_most_common_words(tweets):
    compile_text = ''
    word_count_dict_list = []
    for tweet in tweets:
        compile_text += tweet.clean_text.lower()
    counted_list = Counter(compile_text.split()).most_common()
    for pair in counted_list:
        if pair[0].lower() not in common_English_words and pair[1] > 2:
            set_dict = {'parcel': 'phrase', 'text': pair[0], 'count': pair[1]}
            word_count_dict_list.append(set_dict)
    print(word_count_dict_list)
    return word_count_dict_list


