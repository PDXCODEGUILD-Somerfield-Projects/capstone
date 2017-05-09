import datetime
import json

import re
from django.test import TestCase

from zeitgeist.twitter_data import deserialized_twitter_data, get_most_common_words, find_most_common_parcels
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

        common_words_text = get_most_common_words(deserialized)
        self.assertEqual(common_words_text, [])

        test_hashtags = find_most_common_parcels(deserialized, 'hashtags')
        self.assertEqual(test_hashtags, [{'parcel': 'hashtag', 'text': 'ProsperityGospel', 'count': 1}])

        test_user_mentions = find_most_common_parcels(deserialized, 'user_mentions')
        self.assertEqual(test_user_mentions, [{'parcel': 'user_mention', 'text': 'StephKralevich', 'count': 1}, {'parcel': 'user_mention', 'text': 'tomgreenlive', 'count': 1}, {'parcel': 'user_mention', 'text':'HeliumComedyPdx', 'count': 1}, {'parcel': 'user_mention', 'text':'LeahTiscione', 'count': 1}, {'parcel': 'user_mention', 'text':'AWS', 'count': 1}, {'parcel': 'user_mention', 'text': 'NASA', 'count': 1}, {'parcel': 'user_mention', 'text':'elementaltech', 'count': 1}])

        test_urls = find_most_common_parcels(deserialized, 'urls')
        self.assertEqual(test_urls, [{'parcel': 'url', 'text': 'https://t.co/EBqERuI3sF', 'count': 1}])

    def test_large_Twitter_JSON_deserialization(self):
        with open ('zeitgeist/test_data2.json') as source2:
            large_data = json.load(source2)
            large_deserialized = deserialized_twitter_data(large_data)

            most_common_words = get_most_common_words(large_deserialized)
            self.assertEqual(most_common_words, [{'parcel': 'phrase', 'text': 'myself', 'count': 11}, {'parcel': 'phrase', 'text': 'friend?', 'count': 10}, {'parcel': 'phrase', 'text': 'eat', 'count': 10}, {'parcel': 'phrase', 'text': 'nra', 'count': 6}, {'parcel': 'phrase', 'text': 'published', 'count': 5}, {'parcel': 'phrase', 'text': 'watch', 'count': 5}, {'parcel': 'phrase', 'text': 'members', 'count': 4}, {'parcel': 'phrase', 'text': 'meeting', 'count': 4}, {'parcel': 'phrase', 'text': 'wayne', 'count': 4}, {'parcel': 'phrase', 'text': 'world', 'count': 4}, {'parcel': 'phrase', 'text': 'found', 'count': 3}, {'parcel': 'phrase', 'text': 'women', 'count': 3}, {'parcel': 'phrase', 'text': 'back', 'count': 3}, {'parcel': 'phrase', 'text': 'people', 'count': 3}, {'parcel': 'phrase', 'text': 'city', 'count': 3}, {'parcel': 'phrase', 'text': 'addresses', 'count': 3}, {'parcel': 'phrase', 'text': '2017', 'count': 3}, {'parcel': 'phrase', 'text': 'stories', 'count': 3}, {'parcel': 'phrase', 'text': 'good', 'count': 3}, {'parcel': 'phrase', 'text': 'body', 'count': 3}, {'parcel': 'phrase', 'text': 'nothing', 'count': 3}, {'parcel': 'phrase', 'text': 'touch', 'count': 2}, {'parcel': 'phrase', 'text': 'resistance', 'count': 2}, {'parcel': 'phrase', 'text': 'criminal', 'count': 2}, {'parcel': 'phrase', 'text': 'justice', 'count': 2}, {'parcel': 'phrase', 'text': 'executive', 'count': 2}, {'parcel': 'phrase', 'text': 'vice', 'count': 2}, {'parcel': 'phrase', 'text': 'president', 'count': 2}, {'parcel': 'phrase', 'text': 'lapierre', 'count': 2}, {'parcel': 'phrase', 'text': 'hot', 'count': 2}, {'parcel': 'phrase', 'text': 'read', 'count': 2}, {'parcel': 'phrase', 'text': 'shit', 'count': 2}, {'parcel': 'phrase', 'text': 'anyone', 'count': 2}, {'parcel': 'phrase', 'text': 'human', 'count': 2}, {'parcel': 'phrase', 'text': 'bubble', 'count': 2}, {'parcel': 'phrase', 'text': 'bath', 'count': 2}, {'parcel': 'phrase', 'text': 'full', 'count': 2}, {'parcel': 'phrase', 'text': 'massage', 'count': 2}, {'parcel': 'phrase', 'text': 'team', 'count': 2}, {'parcel': 'phrase', 'text': 'those', 'count': 2}, {'parcel': 'phrase', 'text': 'other', 'count': 2}, {'parcel': 'phrase', 'text': 'almost', 'count': 2}, {'parcel': 'phrase', 'text': 'ruin', 'count': 2}, {'parcel': 'phrase', 'text': 'family', 'count': 2}, {'parcel': 'phrase', 'text': 'computer', 'count': 2}, {'parcel': 'phrase', 'text': 'trying', 'count': 2}, {'parcel': 'phrase', 'text': 'download', 'count': 2}, {'parcel': 'phrase', 'text': 'lil', 'count': 2}, {'parcel': 'phrase', 'text': 'records', 'count': 2}, {'parcel': 'phrase', 'text': 'turned', 'count': 2}, {'parcel': 'phrase', 'text': 'soulja', 'count': 2}, {'parcel': 'phrase', 'text': 'boy', 'count': 2}, {'parcel': 'phrase', 'text': 'girl', 'count': 2}, {'parcel': 'phrase', 'text': 'near', 'count': 2}, {'parcel': 'phrase', 'text': 'af', 'count': 2}, {'parcel': 'phrase', 'text': 'thanks', 'count': 2}, {'parcel': 'phrase', 'text': 'dead', 'count': 2}, {'parcel': 'phrase', 'text': 'inside', 'count': 2}, {'parcel': 'phrase', 'text': 'save', 'count': 2}, {'parcel': 'phrase', 'text': 'ryan', 'count': 2}, {'parcel': 'phrase', 'text': 'zinke', 'count': 2}, {'parcel': 'phrase', 'text': 'leadership', 'count': 2}, {'parcel': 'phrase', 'text': 'forum', 'count': 2}, {'parcel': 'phrase', 'text': 'last', 'count': 2}, {'parcel': 'phrase', 'text': 'way', 'count': 2}, {'parcel': 'phrase', 'text': 'trump', 'count': 2}, {'parcel': 'phrase', 'text': 'class', 'count': 2}, {'parcel': 'phrase', 'text': 'matters', 'count': 2}, {'parcel': 'phrase', 'text': 'cool', 'count': 2}, {'parcel': 'phrase', 'text': 'talent', 'count': 2}, {'parcel': 'phrase', 'text': 'help', 'count': 2}, {'parcel': 'phrase', 'text': 'largest', 'count': 2}, {'parcel': 'phrase', 'text': 'riley', 'count': 2}])

            large_test_hashtags = find_most_common_parcels(large_deserialized, 'hashtags')
            self.assertEqual(large_test_hashtags, [{'parcel': 'hashtag', 'text': 'bot', 'count': 1}, {'parcel': 'hashtag', 'text': 'supercorp', 'count': 1}, {'parcel': 'hashtag', 'text': 'KyGan', 'count': 1}, {'parcel': 'hashtag', 'text': 'TheArrangement', 'count': 1}, {'parcel': 'hashtag', 'text': 'LivingDream', 'count': 1}, {'parcel': 'hashtag', 'text': 'MTVAwards', 'count': 1}, {'parcel': 'hashtag', 'text': 'DianaLast100Days', 'count': 1}, {'parcel': 'hashtag', 'text': 'Paris', 'count': 1}, {'parcel': 'hashtag', 'text': 'climate', 'count': 1}, {'parcel': 'hashtag', 'text': 'agreement', 'count': 1}])

            large_test_user_mentions = find_most_common_parcels(large_deserialized, 'user_mentions')
            self.assertEqual(large_test_user_mentions, [{'parcel': 'user_mention', 'text': 'heIIarelates', 'count': 10}, {'parcel': 'user_mention', 'text': 'pdxlawgrrrl', 'count': 2}, {'parcel': 'user_mention', 'text': 'rasmussenriley', 'count': 2}, {'parcel': 'user_mention', 'text': 'FryinHam', 'count': 2}, {'parcel': 'user_mention', 'text': 'BeingDetained', 'count': 2}, {'parcel': 'user_mention', 'text': 'ErinLOLiver', 'count': 2}, {'parcel': 'user_mention', 'text': 'SallyAlbright', 'count': 2}, {'parcel': 'user_mention', 'text': 'Malinasaval', 'count': 2}, {'parcel': 'user_mention', 'text': '_calev', 'count': 2}, {'parcel': 'user_mention', 'text': 'DiamondJJustice', 'count': 1}])

            large_test_urls = find_most_common_parcels(large_deserialized, 'urls')
            self.assertEqual(large_test_urls, [{'parcel': 'url', 'text': 'https://t.co/nptlWdzSR0', 'count': 10}, {'parcel': 'url', 'text': 'https://t.co/R7EcdkWknU', 'count': 5}, {'parcel': 'url', 'text': 'https://t.co/VAysbts8zo', 'count': 2}, {'parcel': 'url', 'text': 'https://t.co/DB69KhbOg9', 'count': 1}, {'parcel': 'url', 'text': 'https://t.co/YQD4bFSq5o', 'count': 1}, {'parcel': 'url', 'text': 'https://t.co/LmINSe0i8e', 'count': 1}, {'parcel': 'url', 'text': 'https://t.co/MBaBlPrXxw', 'count': 1}, {'parcel': 'url', 'text': 'https://t.co/JIycjTFKwy', 'count': 1}, {'parcel': 'url', 'text': 'https://t.co/bLXpOeYYis', 'count': 1}, {'parcel': 'url', 'text': 'https://t.co/E7egMNHDAM', 'count': 1}])
