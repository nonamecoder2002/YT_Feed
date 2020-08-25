from pytube import YouTube


import requests


def get_vid_data(v_id: str):
    yt = YouTube(url='https://www.youtube.com/watch?v=' + v_id)
    v_url = yt.streams.filter(
        fps=30,
        resolution='720p',
        file_extension='mp4',
        progressive=True
    ).first().url
    return {
        'v_url': v_url,
        'author': yt.author,
        'title': yt.title,
        'desc': '\n'.join(yt.description.split('\n')[:3])
    }


def downloader(i_stream, v_url):
    req = requests.get(url=v_url, stream=True)
    for chunk in req.iter_content(chunk_size=1024):
        i_stream.write(chunk)
        del chunk
