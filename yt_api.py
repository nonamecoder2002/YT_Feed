from googleapiclient.discovery import build
from Modules.Classes import KeyExpired

from Modules.Classes import Key

api_keys = [
    Key(value='AIzaSyBTZ9drxqXKkh8yijdYaBQS1ijANQQApZQ'),
    Key(value='AIzaSyBtNGfLBehI11PeOeInuyXviPWTE3tglrM')
]


def build_service(keys: list):
    for key in keys:
        if key.is_valid():
            key.use()
            return build(serviceName='youtube', version='v3', developerKey=key.key_value)


channel_pool = [
    # {'id': 'UCGBFIBxDuaEmrL5CxXSxx6g', 'name': 'СТАС'},
    # {'id': 'UCptRK95GEDXvJGOQIFg50fg', 'name': 'Игорь Линк'},
    # {'id': 'UC9MK8SybZcrHR3CUV4NMy2g', 'name': 'Диджитализируй!'},
    # {'id': 'UCPIKvg4P2pRDdmyN1gi9bnA', 'name': 'MovieMaker'},
    {'id': 'UCg0bIYJXvberMBRdO1k1Dxg', 'name': 'Izzy ᴸᴬᴵᶠ'},
    # {'id': 'UC1qWaT8_iPHSBYgB4T2ltuA', 'name': 'Ай, Как Просто!'},
    # {'id': 'UCCezIgC97PvUuR4_gbFUs5g', 'name': 'Corey Schafer'},
    # {'id': 'UCq7JZ8ATgQWeu6sDM1czjhg', 'name': 'StopGame.Ru'},
    # {'id': 'UC9DXAsBD4-ITVuvpd68401Q', 'name': 'AutoTopNL'},
    # {'id': 'UCspfe9lef7ApJaHQsOcPC1A', 'name': 'overbafer1'}
]

latest_video_pool = []

# Will be called once per hour!!!


def search_latest(channel_id: str):

    youtube = build_service(keys=api_keys)
    if youtube is None:
        raise KeyExpired
    else:
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            order='date',
            maxResults=1
        )
        response = request.execute()

        return response


def parse_response_item(response_item_: dict):
    item_snippet = response_item_['snippet']
    video_id = response_item_['id']['videoId']
    parse_result = {
        'video_id': video_id,
        'video_url': 'https://www.youtube.com/watch?v=' + video_id,
        'video_title': item_snippet['title'],
        'video_description': item_snippet['description'],
        'video_preview': item_snippet['thumbnails']['high']['url']
    }
    return parse_result


for channel in channel_pool:
    response_item = search_latest(channel_id=channel['id'])['items'][0]
    video_dict = parse_response_item(response_item_=response_item)
    dict_entity = dict(yt_id=channel['name'], video_id=video_dict['video_id'])
    latest_video_pool.append(dict_entity)
    print(
        channel['name'], '\n\t',
        video_dict['video_title'], '\n',
        video_dict['video_preview'], '\n\n',
        video_dict['video_url'], '\n',
    )
    print('\n\n', latest_video_pool)
