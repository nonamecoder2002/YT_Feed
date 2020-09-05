import logging

from pytube import YouTube


logger = logging.getLogger(__name__)

logger.setLevel(logging.ERROR)

formatter = logging.Formatter('%(levelname)s-->%(asctime)s: %(name)s: %(message)s')

file_handler = logging.FileHandler('logs.txt', mode='a')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
        if stream.filesize_approx > 52000000:
            broken = True
        return {
            'v_url': stream.url,
            'title': f'<b>{yt.title}</b>',
            'desc': '\n'.join(yt.description.split('\n')[:3])[:150] + '...',
            'broken': broken
        }
    except Exception as exc:
        logger.exception(exc)
