from googleapiclient.discovery import build


def build_service(keys: list):
    for key in keys:
        if key.is_valid():
            key.use()
            return build(serviceName='youtube', version='v3', developerKey=key.key_value, cache_discovery=False)


def get_playlist(_channel_id: str, _keys: list):

    service = build_service(keys=_keys)

    request = service.channels().list(
        part="contentDetails",
        id=_channel_id,
        maxResults=1
    )

    return request.execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']


def fetch_uploads(channel_id: str, keys: list, out: list):

    service = build_service(keys=keys)

    uploads_pl = get_playlist(_channel_id=channel_id, _keys=keys)

    request = service.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_pl,
        maxResults=3
    )

    for item in request.execute()['items']:

        out.append(item['contentDetails']['videoId'])


def fetch_lat(channel_id: str, keys: list):

    service = build_service(keys=keys)

    uploads_pl = get_playlist(_channel_id=channel_id, _keys=keys)

    request = service.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_pl,
        maxResults=1
    )

    return request.execute()['items'][0]['contentDetails']['videoId']
