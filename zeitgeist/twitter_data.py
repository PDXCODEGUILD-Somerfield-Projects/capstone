import json
import re


def parse_twitter_data(twitter_dump):
    # rt_list = []
    # for statuses in twitter_dump['statuses']:
    #     words = statuses['text']
    #     rt_id = re.search(r'(^RT @.*?:\s)', words)
    #     if rt_id:
    #         rt_id_length = rt_id.end()
    #         rt_list.append(rt_id.group()[3:-2])
    #         words = words[rt_id_length:]
    #     print(words)
    # print(rt_list)
    print(json.dumps(twitter_dump))


