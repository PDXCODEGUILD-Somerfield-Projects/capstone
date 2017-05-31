from django.contrib import admin

from . import models

admin.site.register(models.UserProfile)
admin.site.register(models.SearchQuery)
admin.site.register(models.SearchResultSet)
admin.site.register(models.Filter)
admin.site.register(models.ParcelType)
admin.site.register(models.SearchResultItem)