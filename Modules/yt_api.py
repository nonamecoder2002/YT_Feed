# import asyncio

from googleapiclient.discovery import build
from Modules.Classes import KeyExpired


def build_service(keys: list):
    for key in keys:
        if key.is_valid():
            key.use()
            return build(serviceName='youtube', version='v3', developerKey=key.key_value)


def make_video_pool(channel_pool_: list, video_pool_: list, api_keys: list):
    youtube = build_service(keys=api_keys)
    if youtube is None:
        raise KeyExpired
    else:
        for channel in channel_pool_:
            request = youtube.search().list(
                part='snippet',
                channelId=channel['channelId'],
                order='date',
                maxResults=1
            )
            response = request.execute()['items'][0]
            return_ = {
                'channelTitle': response['snippet']['channelTitle'],
                'videoId': response['id']['videoId']
            }
            video_pool_.append(return_)


def get_video_details(api_keys_: list, video_id: str):
    youtube = build_service(keys=api_keys_)
    request = youtube.videos().list(
        part='snippet',
        id=video_id
    )
    response = request.execute()['items'][0]
    return response


# items[0][snippet][channelTitle], items[0][id][videoId]

def make_message_content(response_item_: dict):
    item_snippet = response_item_['snippet']
    video_id = response_item_['id']
    parse_result = {
        'channel_title': item_snippet['channelTitle'],
        'video_url': 'https://www.youtube.com/watch?v=' + video_id,
        'video_title': item_snippet['title'],
        'video_description': item_snippet['description'],
        'video_preview': item_snippet['thumbnails']['maxres']['url']
    }
    return parse_result


# async def update_video_pool(entity: dict, pool: list, latest_pool_: list):
#     for pool_entity in pool:
#         if entity['channelTitle'] == pool_entity['channelTitle']:
#             if entity['videoId'][-1:-4:-1] != pool_entity['videoId'][-1:-4:-1]:
#                 pool.remove(pool_entity)
#                 pool.append(entity)
#                 latest_pool_.append(entity)
#                 return None


# for channel in channel_pool:
#     response_item = make_pool(channel_id=channel['id'])['items'][0]
#     video_dict = parse_response_item(response_item_=response_item)
#     dict_entity = dict(yt_name=channel['name'], video_id=video_dict['video_id'])
#     video_pool.append(dict_entity)
#     print(
#         channel['name'], '\n\t',
#         video_dict['video_title'], '\n',
#         video_dict['video_preview'], '\n\n',
#         video_dict['video_url'], '\n',
#     )
#     print('\n\n', video_pool)
