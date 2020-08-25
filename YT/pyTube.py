from pytube import YouTube


def get_vid_url(vid_id: str):
    download_url = YouTube(url='https://www.youtube.com/watch?v=' + vid_id).streams.filter(
        fps=30,
        resolution='720p',
        file_extension='mp4',
        progressive=True
    ).first().url
    return download_url


def get_vid_info(vid_id: str):
    vid_obj = YouTube(url='https://www.youtube.com/watch?v=' + vid_id)
    return {
        'author': vid_obj.author,
        'title': vid_obj.title,
        'views': vid_obj.views,
    }
