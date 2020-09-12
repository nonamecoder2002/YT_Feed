
from pytube import YouTube

from YT import logger


def get_vid_data(v_id: str):
    broken = False
    try:
        yt = YouTube(url='https://www.youtube.com/watch?v=' + v_id)
        stream = yt.streams.filter(
            fps=30,
            resolution='360p',
            mime_type='video/mp4',
            progressive=True
        ).first()
        if yt.length > 600:
            broken = True
        return {
            'v_url': stream.url,
            't_url': yt.thumbnail_url,
            'title': f'<b>{yt.title}</b>',
            'desc': f'<code>{yt.description[:175]}</code>',
            'broken': broken
        }
    except Exception as exc:

        logger.exception(exc)

        return False
