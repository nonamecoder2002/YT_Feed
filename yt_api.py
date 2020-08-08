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
    {'id': 'UCGBFIBxDuaEmrL5CxXSxx6g', 'name': 'СТАС'},
    # {'id': 'UCptRK95GEDXvJGOQIFg50fg', 'name': 'Игорь Линк'},
    # {'id': 'UC9MK8SybZcrHR3CUV4NMy2g', 'name': 'Диджитализируй!'},
    # {'id': 'UCPIKvg4P2pRDdmyN1gi9bnA', 'name': 'MovieMaker'},
    # {'id': 'UCg0bIYJXvberMBRdO1k1Dxg', 'name': 'Izzy ᴸᴬᴵᶠ'},
    # {'id': 'UC1qWaT8_iPHSBYgB4T2ltuA', 'name': 'Ай, Как Просто!'},
    # {'id': 'UCCezIgC97PvUuR4_gbFUs5g', 'name': 'Corey Schafer'},
    # {'id': 'UCq7JZ8ATgQWeu6sDM1czjhg', 'name': 'StopGame.Ru'},
    # {'id': 'UC9DXAsBD4-ITVuvpd68401Q', 'name': 'AutoTopNL'},
    # {'id': 'UCspfe9lef7ApJaHQsOcPC1A', 'name': 'overbafer1'}
]

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


def video_link(item: dict):
    """
    Creates web-link to the specified video

    :param item: dict
    :return: link: string
    """
    link = 'https://www.youtube.com/watch?v=' + item['id']['videoId']
    return link


def parse_snippet(snippet: dict):
    """
    Parses snippet into a dict of information about certain video


    :param snippet: dict
    :return: parse_result -> dict obj.
    """
    parse_result = {
        'title': snippet['title'],
        'description': snippet['description'],
        'preview': snippet['thumbnails']['high']['url']
    }
    return parse_result


for channelId in channel_pool:
    respond_item = search_latest(channel_id=channelId['id'])['items'][0]
    v_link = video_link(item=respond_item)
    video_dict = parse_snippet(snippet=respond_item['snippet'])
    print(channelId['name'], '\n\t', video_dict['title'], '\n', video_dict['preview'], '\n\n', v_link, '\n')
