import datetime
import json

import re
from django.test import TestCase
from .domain import Post, Parcel, Hashtag, UserMention, Url, Tweet, format_datetime



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
        print(deserialized)

#     def test_twit(self):
#         result = TwittDD().deserialize("{}")
#
#
#     def test_twit_list(self):
#         result_list = TwittListDD().deserialize("[]")
#
# class TwittListDD:
#     def __init__(self, twittDD):
#         self.twittDD = twittDD
#
#     def deserialize(self, json_string):


# def deserialize(self, json_string):
#     json_dict = json.loads(json_string)
#     Tweet(json_dict['name'], None, 'TODO', False, [], [], [])

# my_tweet = Tweet('someguy', some_datetime, 'This guys said some important stuff', False,
#                          [Hashtag('Twitter', 'pdxrocks'), Hashtag('Twitter','codeisawesome')],
#                          [UserMention('Twitter', 'somedude'), UserMention('Twitter', 'pythongal')],
#                          [Url('Twitter', 'https://t.co/Ymtxgvdx2u')])

def deserialized_twitter_data(data):
    user_name = ''
    post_time = datetime
    raw_text = ''
    is_retweet = False
    tweets = []

    for tweet in data.get('statuses'):

        hashtags = []
        hashtag_indices = []
        user_mentions = []
        user_mention_indices = []
        urls = []
        url_indices = []
        tweet_indices_list = []

        user_name = tweet['user']['screen_name']
        post_time = format_datetime(tweet['created_at'])
        raw_text = tweet['text']
        is_retweet = True if 'retweeted_status' in tweet else False

        tweet_hashtag_list = []
        hashtag_indices_list = []
        for tag in tweet.get('entities')['hashtags']:
            tweet_hashtag_list.append(tag['text'])
            hashtag_indices_list.append(tag['indices'])
        hashtags += tweet_hashtag_list
        hashtag_indices += hashtag_indices_list

        tweet_user_mention_list = []
        user_mention_indices_list = []
        for mention in tweet['entities']['user_mentions']:
            tweet_user_mention_list.append(mention['screen_name'])
            user_mention_indices_list.append(mention['indices'])
        user_mentions += tweet_user_mention_list
        user_mention_indices += user_mention_indices_list

        url_indices_list = []
        tweet_url_list = []
        for url in tweet.get('entities')['urls']:
            tweet_url_list.append(url['url'])
            url_indices_list.append(url['indices'])
        urls += tweet_url_list


        # create a string of 'clean' text for parsing later
        clean_text = ''

        # add all of the tweet indices to one list and sort it
        tweet_indices_list = hashtag_indices_list + user_mention_indices_list + url_indices_list
        tweet_indices_list.sort()
        # loop through the raw_text and add the text between hashtags, user_mentions, and urls to clean_text
        for num, index in enumerate(tweet_indices_list):
            if num == 0:
                clean_text = raw_text[0:index[0]]
            else:
                clean_text += raw_text[tweet_indices_list[num - 1][1]: tweet_indices_list[num][0]]
            if num == len(tweet_indices_list) - 1:
                clean_text += raw_text[tweet_indices_list[num][1]:len(raw_text)]
        # use regex to make these more readable
        if is_retweet == True:
            clean_text = re.sub(r'^RT\s:\s', '', clean_text)
        clean_text = re.sub(r'\sb/c\s', ' because ', clean_text)
        clean_text = re.sub(r'\s&amp;\s', ' and ', clean_text)
        clean_text = re.sub(r'\s+', ' ', clean_text)

        new_tweet = Tweet(user_name, post_time, raw_text, is_retweet, hashtags, user_mentions, urls, clean_text)

        tweets.append(new_tweet)

    return tweets

