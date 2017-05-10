from .models import User, SearchQuery, SearchResultSet, SearchResultItem, Filter, ParcelType

def pull_queries_by_user(user):
    user_queries = SearchQuery.objects.filter(searchresultset__user=user)
    print(user_queries)
    return user_queries