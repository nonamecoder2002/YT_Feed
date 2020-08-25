from YT.yt_api import (
    latest_vid_id,
    compare
)

from YT.pyTube import (
    get_vid_url,
    get_vid_info
)


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


def vid_data(video_id: str):
    video = get_vid_url(vid_id=video_id)
    # vid_details = get_vid_info(vid_id=video_id)
    return {
        'video_url': video,
        # 'vid_details': vid_details
    }
# for 2 req instantly goes BAN!