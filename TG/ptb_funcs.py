import requests

import os

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from YT.pyTube import (
    get_vid_data
)


def del_mes(_update, _context):
    mes_id = _update.message.message_id
    _context.bot.delete_message(
        chat_id=399835396,
        message_id=mes_id

    )


def dl_vid(file_path: str, v_url: str):
    max_size = 52000000
    chunk_size = 2000
    req = requests.get(url=v_url, stream=True)
    with open(file_path, 'wb') as file:
        for chunk in req.iter_content(chunk_size=chunk_size):
            if max_size - chunk_size >= 0:
                file.write(chunk)
            else:
                break
            max_size = max_size - chunk_size


def send_video(context, v_id: str, f_path_, clip_path):

    keyboard = [[InlineKeyboardButton(text='❌ Delete', callback_data='del')]]
    v_data = get_vid_data(v_id=v_id)
    dl_vid(file_path=f_path_, v_url=v_data['v_url'])
    ffmpeg_extract_subclip(filename=f_path_, t1=0, t2=800, targetname=clip_path)
    os.remove(f_path_)
    caption = v_data['title'] + '\n\n' + v_data['desc']
    if v_data['broken']:
        keyboard.insert(
            0,
            [InlineKeyboardButton(text='📺 Watch Full', url=f'https://www.youtube.com/watch?v={v_id}&t={800}')]
        )
    markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_video(
        chat_id='399835396',
        video=open(clip_path, 'rb'),
        caption=caption,
        supports_streaming=True,
        parse_mode='HTML',
        reply_markup=markup
    )
    os.remove(clip_path)
