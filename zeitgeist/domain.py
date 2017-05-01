from datetime import datetime
import re

class Parcel(object):
    '''A trackable 'unit' of a social media post (hashtag, url, etc)

    Attributes:
        type: string representing parcel type (hashtag, url, etc)
        text: string of the parcel contents
    '''
    def __init__(self, category, text):
        self.category = category
        self.text = text

    def __repr__(self):
        return 'Parcel({!r}: {!r}'.format(
            self.category,
            self.text,
        )

    def __eq__(self, other):
        return (
            self.category == other.category and
            self.text == other.text
        )

class Hashtag(Parcel):
    '''A hashtag entity

    Attributes:
        category: set to 'hashtag'
        (inherits text from Parcel)
    '''
    def __init__(self, category, text):
        Parcel.__init__(self, 'hashtag', text)

    def __repr__(self):
        return '#' + self.text

    def __eq__(self, other):
        return (
            self.category == other.category and
            self.text == other.text
        )

class UserMention(Parcel):
    '''A 'user mention' entity

    Attributes:
        category: set to 'user_mention'
        (inherits text from Parcel)
    '''

    def __init__(self, category, text):
        Parcel.__init__(self, 'user_mention', text)

    def __repr__(self):
        return '@' + self.text

    def __eq__(self, other):
        return (
            self.category == other.category and
            self.text == other.text
        )

class Url(Parcel):
    '''A 'url' entity

    Attributes:
        category: set to 'url'
        (inherits text from Parcel)
    '''

    def __init__(self, category, text):
        Parcel.__init__(self, 'url', text)

    def __repr__(self):
        return self.text

    def __eq__(self, other):
        return (
            self.category == other.category and
            self.text == other.text
        )

class Post(object):
    '''A social media post, such as a 'tweet', instagram 'share', etc

    Attributes:
        platform: social media platform the post was from
        user_name: user handle from social media platform
        post_time: UTC time it was posted
        text: text in the post

    '''
    def __init__(self, platform, user_name, post_time, raw_text):
        self.platform = platform
        self.user_name = user_name
        self.post_time = post_time
        self.raw_text = raw_text

    def __repr__(self):
        date_str_format = '%m/%d/%y %H:%M:%S %Z'
        formatted_post_time = datetime.strftime(self.post_time, date_str_format)
        return 'Post(' + self.platform + ', ' + formatted_post_time + ', @' + self.user_name + ', ' + self.raw_text + ')'

    def __eq__(self, other):
        return (
            self.platform == other.platform and
            self.user_name == other.user_name and
            self.post_time == other.post_time and
            self.raw_text == other.raw_text
        )

class Tweet(Post):
    '''Twitter 'post' object (a 'tweet')

    Attributes:
        retweet: True/False boolean
        hashtags: list of hashtags
        user_mentions: list of user_mentions
        urls: list of urls
    '''
    def __init__(self, user_name, post_time, raw_text, is_retweet, hashtags, user_mentions, urls, clean_text):
        Post.__init__(self, 'Twitter', user_name, post_time, raw_text)
        self.is_retweet = is_retweet
        self.hashtags = hashtags
        self.user_mentions = user_mentions
        self.urls = urls
        self.clean_text = clean_text

    def __repr__(self):
        date_str_format = '%m/%d/%y %H:%M:%S %Z'
        formatted_post_time = datetime.strftime(self.post_time, date_str_format)

        return 'Tweet(' + formatted_post_time + ', @' + self.user_name + ', ' + self.raw_text + ', '\
               + str(self.is_retweet) + ', ' + str(self.hashtags) + ', ' + str(self.user_mentions) + ', '\
               + str(self.urls) + ', ' + self.clean_text + ')'


    def __eq__(self, other):
        return (
            self.user_name == other.user_name and
            self.post_time == other.post_time and
            self.raw_text == other.raw_text and
            self.is_retweet == other.is_retweet and
            self.hashtags == other.hashtags and
            self.user_mentions == other.user_mentions and
            self.urls == other.urls
        )


# Twitter dates are all in UTC time - they use browser timezone to delta 'time since'
def format_datetime(datetime_str):
    formatted_post_time = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %z %Y')
    # 'Wed Apr 26 17:43:16 +0000 2017'
    return formatted_post_time
