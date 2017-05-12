from .models import User, SearchQuery, SearchResultSet, SearchResultItem, Filter, ParcelType

def pull_queries_by_user(user):
    user_queries = SearchQuery.objects.filter(searchresultset__user=user)
    print(user_queries)
    return user_queries

def rebuild_query_by_id(search_id):
    query_list = []
    lat = SearchQuery.objects.get(id=search_id).latitude
    lng = SearchQuery.objects.get(id=search_id).longitude
    result_items_set = SearchResultItem.objects.filter(search_result__search_query_id=search_id)
    for item in result_items_set:
        parcel = ParcelType.objects.select_related('search_result_item').get(id=item.id).parcel_type
        dict_item = {'parcel': parcel, 'text': item.item_text, 'count': item.item_count}
        query_list.append(dict_item)
    query_dict = {'lat': lat, 'lng': lng, 'twitter': query_list}
    print(query_dict)
    return query_dict

def delete_selected_queries(id_array):
    sq = SearchQuery.objects.filter(pk__in=id_array)
    sq.delete()
