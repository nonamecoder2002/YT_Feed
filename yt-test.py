from googleapiclient.discovery import build

api_key = 'AIzaSyCiqyUzl_r7ZJvmcuf1HmMnLVIapwTDWlg'

youtube = build(serviceName='youtube', version='v3', developerKey=api_key)

channel_id_pool = [
    'UCGBFIBxDuaEmrL5CxXSxx6g',
    'UCptRK95GEDXvJGOQIFg50fg',
    'UC9MK8SybZcrHR3CUV4NMy2g',
    'UCPIKvg4P2pRDdmyN1gi9bnA',
    'UCg0bIYJXvberMBRdO1k1Dxg',
    'UC1qWaT8_iPHSBYgB4T2ltuA',
    'UCCezIgC97PvUuR4_gbFUs5g',
    'UCq7JZ8ATgQWeu6sDM1czjhg',
    'UC9DXAsBD4-ITVuvpd68401Q',
    'UCspfe9lef7ApJaHQsOcPC1A'

]

# channel_name_pool = []
# def get_id(name: str):
#     request = youtube.channels().list(
#         part='id',
#         forUsername=name
#     )
#     return request.execute()
#
#
# for name in channel_name_pool:
#     print(get_id(name=name)['items'][0]['id'], '\n')


def search_latest(channel_id: str):
    request = youtube.search().list(
        part='snippet',
        channelId=channel_id,
        order='date',
        maxResults=1
    )
    return request.execute()


def video_link(item: dict):
    link = 'https://www.youtube.com/watch?v=' + item['id']['videoId']
    return link


def parse_snippet(snippet: dict):
    parse_result = {
        # 'published': snippet['publishedAt'],
        'title': snippet['title'],
        'description': snippet['description'],
        'preview': snippet['thumbnails']['high']['url'],
        'channel_name': snippet['channelTitle']
    }
    return parse_result


for channelId in channel_id_pool:
    respond_item = search_latest(channel_id=channelId)['items'][0]
    v_link = video_link(item=respond_item)
    video_dict = parse_snippet(snippet=respond_item['snippet'])
    print(video_dict['channel_name'], '\n\t', video_dict['title'], '\n', video_dict['preview'], '\n\n', v_link, '\n')
