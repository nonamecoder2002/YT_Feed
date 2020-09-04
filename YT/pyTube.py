import logging

from pytube import YouTube


logger = logging.getLogger(__name__)

logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s-->%(asctime)s: %(name)s: %(message)s')

file_handler = logging.FileHandler('logs.txt', mode='a')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def get_vid_data(v_id: str):
    try:
        yt = YouTube(url='https://www.youtube.com/watch?v=' + v_id)
        v_url = yt.streams.filter(
            fps=30,
            resolution='360p',
            mime_type='video/mp4',
            progressive=True
        ).first().url
        return {
            'v_url': v_url,
            'title': f'<b>{yt.title}</b>',
            'desc': '\n'.join(yt.description.split('\n')[:3])[:200] + '...'
        }
    except Exception as exc:
        logger.exception(exc)
