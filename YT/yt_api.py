from googleapiclient.discovery import build


def build_service(keys: list):
    for key in keys:
        if key.is_valid():
            key.use()
            return build(serviceName='youtube', version='v3', developerKey=key.key_value)


def latest_vid_id(channel_id: str, keys: list):
    service = build_service(keys=keys)
    request = service.channels().list(
        part="contentDetails",
        id=channel_id,
        maxResults=1
    )

    playlist_id = request.execute()['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    request2 = service.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id,
        maxResults=1
    )

    lat_vid_id = request2.execute()['items'][0]['contentDetails']['videoId']

    return lat_vid_id


def compare(old_pool: list, new_pool: list, output_pool: list):
    for i in range(len(old_pool)):
        if old_pool[i] != new_pool[i]:
            output_pool.append(new_pool[i])


def locator(channel_pool: list, perm_video_pool: list, api_keys: list):
    temp_video_pool, latest_video_pool = [], []
    for _channel in channel_pool:
        _latest_v_id = latest_vid_id(channel_id=_channel['channelId'], keys=api_keys)
        temp_video_pool.append(_latest_v_id)
    compare(old_pool=perm_video_pool, new_pool=temp_video_pool, output_pool=latest_video_pool)
    return [
        latest_video_pool,
        temp_video_pool
    ]
