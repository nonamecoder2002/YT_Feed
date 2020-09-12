from googleapiclient.discovery import build

from googleapiclient.errors import HttpError

from . import logger


def build_service(keys: list):

    for key in keys:
        if key.is_valid():
            return build(serviceName='youtube', version='v3', developerKey=key.value, cache_discovery=False)


def execute_req(req, keys: list):

    for key in keys:
        if key.is_valid():
            try:
                return req.execute()

            except HttpError:
                key.expire()
                logger.warning(f'Key Expired {key.value}')
        else:
            try:
                resp = req.execute()
                key.mk_valid()
                logger.warning(f'Key Renewed {key.value}')
                return resp

            except HttpError:
                pass


def get_playlist(_channel_id: str, _keys: list):

    service = build_service(keys=_keys)
    request = service.channels().list(
        part="contentDetails",
        id=_channel_id,
        maxResults=1
    )

    return execute_req(req=request, keys=_keys)['items'][0]['contentDetails']['relatedPlaylists']['uploads']


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


def fetch_lat(channel_id: str, keys_: list):

    service = build_service(keys=keys_)

    uploads_pl = get_playlist(_channel_id=channel_id, _keys=keys_)

    request = service.playlistItems().list(
        part="contentDetails",
        playlistId=uploads_pl,
        maxResults=1
    )

    return execute_req(req=request, keys=keys_)['items'][0]['contentDetails']['videoId']
