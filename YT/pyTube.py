from pytube import YouTube


def get_vid_data(v_id: str):
    yt = YouTube(url='https://www.youtube.com/watch?v=' + v_id)
    v_url = yt.streams.filter(
        fps=30,
        resolution='360p',
        mime_type='video/mp4',
        progressive=True
    ).first().url
    return {
        'v_url': v_url,
        'author': yt.author,
        'title': f'<b>{yt.title}</b>',
        'desc': '\n'.join(yt.description.split('\n')[:3])
    }
