from pytube import YouTube


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
        'thumbnail_url': yt.thumbnail_url,
        'desc': yt.description.split('\n')[0]
    }


# print(get_vid_data('PJiaw2AnhsU'))