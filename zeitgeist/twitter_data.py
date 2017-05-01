from collections import Counter
from datetime import datetime
import RAKE

import re

from zeitgeist.domain import format_datetime, Tweet, Hashtag, UserMention, Url


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
        clean_text = re.sub(r'\s&amp;\s', ' and ', clean_text)
        clean_text = re.sub(r'(\r\n|\r|\n)|\s{2,}', ' ', clean_text)
        clean_text = re.sub(r'https:.+?\s', ' ', clean_text)

        # create a new tweet object from the deserialized json tweet
        new_tweet = Tweet(user_name, post_time, raw_text, is_retweet, hashtags, user_mentions, urls, clean_text)
        print(clean_text)
        # add the tweet object to a list of tweet objects
        tweets.append(new_tweet)

    return tweets

def pull_tweet_text(tweets):
    '''Uses python-rake to create a list of key words and phrases with ranking

    :param tweets: list of Tweet objects
    :return:
    '''
    compile_text = ''
    for tweet in tweets:
        compile_text += tweet.clean_text
    Rake = RAKE.Rake('zeitgeist/EnglishStopList')
    raked = Rake.run(compile_text)
    # search for most common instances of these words/phrases
    print(compile_text)
    print(raked)

def find_most_common_parcels(tweets, parcel_type):
    '''Finds the 10 most common parcel strings in list of Tweets

    :param tweets: list of Tweet objects
    :param parcel_type: 'hashtags', 'user_mentions', or 'urls'
    :return:
    '''
    parcel_key_dict = {'hashtags': Hashtag, 'user_mentions': UserMention, 'urls': Url}
    all_parcel_list = []
    for tweet in tweets:
        parcel_list = getattr(tweet, parcel_type)
        # [Hashtag('Twitter', 'NewYorkTimes'), Hashtag('Twitter', 'Technology')]
        all_parcel_list += [parcel.text for parcel in parcel_list if len(parcel_list) > 0]
    parcel_dict = Counter(all_parcel_list)
    print(parcel_dict.most_common(10))


