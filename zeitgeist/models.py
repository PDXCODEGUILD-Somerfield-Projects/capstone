from django.db import models
from django.contrib.auth.models import User


class SearchQuery(models.Model):
    user = models.ForeignKey(User)
    timestamp = models.DateTimeField
    profanity_filter = models.NullBooleanField(default=False)
    adult_filter = models.NullBooleanField(default=False)

    def __str__(self):
        return self.user + ' query at ' + self.timestamp

    def __repr__(self):
        return 'SearchQuery(id={!r}, user={!r}, datetime={!r})'.format(
            self.id,
            self.user,
            self.timestamp
        )



class Filter(models.Model):
    word = models.CharField
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
        return self.user + ' result ' + self.search_query

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
    text = models.CharField
    count = models.PositiveSmallIntegerField

    def __str__(self):
        return self.text + ': ' + self.count

    def __repr__(self):
        return 'SearchResultItem(id={!r}, text={!r}, count={!r})'.format(
            self.id,
            self.text,
            self.count
        )


class ParcelType(models.Model):
    parcel_type = models.CharField
    search_result_item = models.ForeignKey(
        SearchResultItem,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.parcel_type

    def __repr__(self):
        return 'ParcelType(id={!r}, parcel_type={!r}, search_result_item={!r})'.format(
            self.id,
            self.parcel_type,
            self.search_result_item
        )



