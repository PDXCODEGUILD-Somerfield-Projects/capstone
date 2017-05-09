from django.contrib import admin

from . import models

admin.site.register(models.SearchQuery)
admin.site.register(models.SearchResults)
admin.site.register(models.Filter)