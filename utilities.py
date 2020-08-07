from googleapiclient.discovery import build

api_key = 'AIzaSyCiqyUzl_r7ZJvmcuf1HmMnLVIapwTDWlg'

youtube = build(serviceName='youtube', version='v3', developerKey=api_key)


channel_name_pool = []


def get_id(name: str):
    request = youtube.channels().list(
        part='id',
        forUsername=name
    )
    return request.execute()


for name in channel_name_pool:
    print(get_id(name=name)['items'][0]['id'], '\n')
