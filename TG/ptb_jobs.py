from . import consts

from YT.yt_api import (
    fetch_uploads,
    fetch_lat
)

from .ptb_funcs import send_video

from telegram.ext import (
    CallbackContext
)

from . import logger


def vid_feed(context: CallbackContext):

    uploads = consts.upload_ls
    api_keys = consts.api_keys_
    channel_pool = consts.channel_pool_

    for _channel in channel_pool:

        v_id = fetch_lat(channel_id=_channel['channelId'], keys_=api_keys)

        if v_id not in uploads:

            logger.info(f'Fetched Video: {v_id}')

            if send_video(context=context, v_id=v_id):

                logger.info(f'Sent Video {v_id}')

                uploads.append(v_id)

            else:
                pass


def get_uploads(context: CallbackContext):
    uploads = consts.upload_ls
    api_keys = consts.api_keys_
    channel_pool = consts.channel_pool_

    uploads.clear()

    for channel in channel_pool:

        fetch_uploads(
            channel_id=channel['channelId'],
            keys=api_keys,
            out=uploads
        )

