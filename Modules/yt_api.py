
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


def compare(old_pool: list, new_pool: list, output_pool: list):
    for i in range(len(old_pool)):
        if old_pool[i]['videoId'] != new_pool[i]['videoId']:
            output_pool.append(new_pool[i])


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
