
from googleapiclient.discovery import build

from YT.Classes import KeyExpired


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
            video_pool_.append(response['id']['videoId'])


def compare(old_pool: list, new_pool: list, output_pool: list):
    for i in range(len(old_pool)):
        if old_pool[i] != new_pool[i]:
            output_pool.append(new_pool[i])
