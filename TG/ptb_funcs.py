import requests

from io import BytesIO


from YT.pyTube import (
    get_vid_data
)


def write_to_stream(i_stream, v_url):
    max_size = 52000000
    chunk_sz = 2000
    req = requests.get(url=v_url, stream=True)
    for chunk in req.iter_content(chunk_size=chunk_sz):
        if max_size - chunk_sz >= 0:
            i_stream.write(chunk)
        else:
            break
        max_size = max_size - chunk_sz


def send_video(context, v_id: str, markup):
    stream = BytesIO()
    v_data = get_vid_data(v_id=v_id)
    write_to_stream(i_stream=stream, v_url=v_data['v_url'])
    stream.seek(0)
    caption = v_data['title'] + '\n\n' + v_data['desc']
    context.bot.send_video(
        chat_id='399835396',
        video=stream,
        caption=caption,
        supports_streaming=True,
        parse_mode='HTML',
        reply_markup=markup
    )
    stream.close()
