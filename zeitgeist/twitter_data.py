from collections import Counter
from datetime import datetime
import RAKE

import re

from .common_English_words import common_English_words
from zeitgeist.domain import format_datetime, Tweet, Hashtag, UserMention, Url

STRIP_STRING = '.,;:!/*()|\'\"[]{}#@&?'

def deserialized_twitter_data(data):
    '''Takes a Twitter data 'blob' and turns it into a list of Tweet objects

    :param data: Twitter data 'blob' from JSON response
    :return:
    '''
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

        # pull information from each tweet in the file
        user_name = tweet['user']['screen_name']
        post_time = format_datetime(tweet['created_at'])
        raw_text = tweet['text']
        is_retweet = True if 'retweeted_status' in tweet else False

        # build a list of hashtags in the tweet
        # and pull a list of their indices in the tweet string
        tweet_hashtag_list = []
        hashtag_indices_list = []
        for tag in tweet.get('entities')['hashtags']:
            this_hashtag = Hashtag('Twitter', tag['text'])
            tweet_hashtag_list.append(this_hashtag)
            hashtag_indices_list.append(tag['indices'])
        hashtags += tweet_hashtag_list
        hashtag_indices += hashtag_indices_list

        # build a list of user_mentions in the tweet
        # and pull a list of their indices in the tweet string
        tweet_user_mention_list = []
        user_mention_indices_list = []
        for mention in tweet['entities']['user_mentions']:
            this_user_mention = UserMention('Twitter', mention['screen_name'])
            tweet_user_mention_list.append(this_user_mention)
            user_mention_indices_list.append(mention['indices'])
        user_mentions += tweet_user_mention_list
        user_mention_indices += user_mention_indices_list

        # build a list of the urls in the tweet
        # and pull a list of their indices in the tweet string
        url_indices_list = []
        tweet_url_list = []
        for url in tweet.get('entities')['urls']:
            this_url = Url('Twitter', url['url'])
            tweet_url_list.append(this_url)
            url_indices_list.append(url['indices'])
        urls += tweet_url_list


        # create a string of 'clean' text for parsing later
        clean_text = ''

        # add all of the tweet indices to one list and sort it
        tweet_indices_list = hashtag_indices_list + user_mention_indices_list + url_indices_list
        tweet_indices_list.sort()
        # loop through the raw_text and add the text between hashtags, user_mentions, and urls to clean_text string
        for num, index in enumerate(tweet_indices_list):
            if num == 0:
                clean_text = raw_text[0:index[0]]
            else:
                clean_text += raw_text[tweet_indices_list[num - 1][1]: tweet_indices_list[num][0]]
            if num == len(tweet_indices_list) - 1:
                clean_text += raw_text[tweet_indices_list[num][1]:len(raw_text)]
        clean_text += ' '
        # use regex to make these more readable
        if is_retweet == True:
            clean_text = re.sub(r'^RT\s:\s', '', clean_text)
        clean_text = re.sub(r'\sb/c\s', ' because ', clean_text)
        clean_text = re.sub(r'\severy1\s', ' everyone ', clean_text)
        clean_text = re.sub(r'\s@\s', ' at ', clean_text)
        clean_text = re.sub(r'\sr\s', ' are ', clean_text)
        clean_text = re.sub(r'(\r\n|\r|\n)|\s{2,}', ' ', clean_text)
        clean_text = re.sub(r'https:.+?\s', ' ', clean_text)
        clean_text = re.sub(r'…|-|//|', '', clean_text)

        # create a new tweet object from the deserialized json tweet
        new_tweet = Tweet(user_name, post_time, raw_text, is_retweet, hashtags, user_mentions, urls, clean_text)
        # add the tweet object to a list of tweet objects
        tweets.append(new_tweet)
    print(tweets)

    return tweets


def pull_tweet_text(tweets):
    '''Uses python-rake to create a list of key words and phrases with ranking

    :param tweets: list of Tweet objects
    :return:
    '''
    compile_text = ''
    rake_count_dict_list = []
    for tweet in tweets:
        compile_text += tweet.clean_text
    Rake = RAKE.Rake('zeitgeist/EnglishStopList')
    raked = Rake.run(compile_text)
    # counts occurrences of each phrase/word from raked in the compiled text
    # creates a tuple list of phrases/words and count (if the count is greater than 1)
    for pair in raked:
        rake_num = compile_text.count(pair[0])
        if rake_num > 1:
            set_rake_dict = {'text': pair[0], 'count': rake_num}
            rake_count_dict_list.append(set_rake_dict)
    return rake_count_dict_list


def get_most_common_words(tweets):
    compile_list = []
    word_count_dict_list = []
    # get the clean text from tweets, change them to lowercase, and make a list of words
    for tweet in tweets:
        words_list = (tweet.clean_text.lower()).split()
        # strip the punctuation from start, end of words
        for word in words_list:
            this_word = word.strip(STRIP_STRING)
            # add words that are not in the common English words list
            if this_word != '' and this_word not in common_English_words:
                compile_list.append(this_word)
    # count each word in the list and return a tupled list with each word and count
    counted_list = Counter(compile_list).most_common()
    # cycle through the list of words and create a dictionary
    # in the {'parcel': 'phrase', 'text': 'word...', 'count': 2} format
    for pair in counted_list:
        if pair[1] > 1:
            set_dict = {'parcel': 'phrase', 'text': pair[0], 'count': pair[1]}
            word_count_dict_list.append(set_dict)
    return word_count_dict_list


def find_most_common_parcels(tweets, parcel_type):
    '''Finds the 10 most common parcel strings in list of Tweets

    :param tweets: list of Tweet objects
    :param parcel_type: 'hashtags', 'user_mentions', or 'urls'
    :return:
    '''
    # dict to match category to parcel object
    parcel_key_dict = {'hashtags': Hashtag, 'user_mentions': UserMention, 'urls': Url}
    all_parcel_list = []
    most_common_dict_list = []
    # runs through the tweet objects in the list
    for tweet in tweets:
        # if the parcel list is not empty, throws the parcel text into a list
        parcel_list = getattr(tweet, parcel_type)
        all_parcel_list += [parcel.text for parcel in parcel_list if len(parcel_list) > 0]
    # counts the occurrences of each parcel
    parcel_count_list = Counter(all_parcel_list)
    # returns the 10 most common parcels in [('phrase', 3), ('word', 2)] format
    most_common =  parcel_count_list.most_common(10)
    # # create variable for each parcel: hashtags --> hashtag, user_mentions --> user_mention, etc.
    parcel = str(parcel_type)[:-1]
    # cycle through the most_common list to create a dictionary
    # in {'parcel': 'hashtag', 'text': 'some-phrase', 'count': 2} format
    for pair in most_common:
        set_dict = {'parcel': parcel, 'text': pair[0], 'count': pair[1]}
        most_common_dict_list.append(set_dict)
    return most_common_dict_list




