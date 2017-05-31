from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user= models.OneToOneField(User)
    twitter_id = models.CharField(max_length=140, default='<empty>')

    def __str__(self):
        return self.user.username + ' twitter_id:' + self.twitter_id

    def __repr__(self):
        return self.twitter_id


class SearchQuery(models.Model):
    user = models.ForeignKey(User)
    query_timestamp = models.DateTimeField('query time')
    profanity_filter = models.NullBooleanField(default=False)
    adult_filter = models.NullBooleanField(default=False)
    latitude = models.FloatField(null=True, blank=True, default=None)
    longitude = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.user.username + ' query at ' + str(self.query_timestamp)

    def __repr__(self):
        return 'SearchQuery(id={!r}, user={!r}, datetime={!r}), lat={!r}, lng={!r}'.format(
            self.id,
            self.user,
            self.query_timestamp,
            self.latitude,
            self.longitude
        )



class Filter(models.Model):
    word = models.CharField(max_length=140, default='<empty>')
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.word

    def __repr__(self):
        return 'Filter(id={!r}, word={!r}, search_query={!r})'.format(
            self.id,
            self.word,
            self.search_query
        )


class SearchResultSet(models.Model):
    search_query = models.ForeignKey(
        SearchQuery,
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(User)

    def __str__(self):
        return 'result ' + str(self.search_query)

    def __repr__(self):
        return 'SearchResult(id={!r}, search_query={!r}, user={!r})'.format(
            self.id,
            self.search_query,
            self.user
        )


class SearchResultItem(models.Model):
    search_result = models.ForeignKey(
        SearchResultSet,
        on_delete=models.CASCADE
    )
    item_text = models.CharField(max_length=140, default='<empty>')
    item_count = models.IntegerField(default=0)

    def __str__(self):
        return self.item_text + ': ' + str(self.item_count)

    def __repr__(self):
        return 'SearchResultItem(id={!r}, text={!r}, count={!r})'.format(
            self.id,
            self.item_text,
            self.item_count
        )


class ParcelType(models.Model):
    parcel_type = models.CharField(max_length=100, default='phrase')
    search_result_item = models.ForeignKey(
        SearchResultItem,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.parcel_type)

    def __repr__(self):
        return 'ParcelType(id={!r}, parcel_type={!r}, search_result_item={!r})'.format(
            self.id,
            self.parcel_type,
            self.search_result_item
        )



