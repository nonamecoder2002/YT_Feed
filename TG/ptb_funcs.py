import shutil

import os

import requests

from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

from PIL import Image

from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from YT.pyTube import (
    get_vid_data
)
from TG import logger


def del_mes(_update, _context):
    mes_id = _update.message.message_id
    _context.bot.delete_message(
        chat_id=399835396,
        message_id=mes_id

    )


def dl_thumb(url_):

    req = requests.get(url=url_)

    with open('./Temp/thumb.jpg', 'wb') as f:
        f.write(req.content)

    thumb = Image.open('./Temp/thumb.jpg')

    thumb.thumbnail((320, 320))

    thumb.save('./Temp/thumb.jpg')


def dl_vid(v_url: str):
    max_size = 52000000
    chunk_size = 2000
    req = requests.get(url=v_url, stream=True)
    with open('./Temp/video.mp4', 'wb') as file:
        for chunk in req.iter_content(chunk_size=chunk_size):
            if max_size - chunk_size >= 0:
                file.write(chunk)
            else:
                break
            max_size = max_size - chunk_size


def send_video(context, v_id: str):
    f_path = './Temp/video.mp4'
    t_path = './Temp/thumb.jpg'
    cl_path = './Temp/clip.mp4'
    try:
        keyboard = [
            [InlineKeyboardButton(text='📺 Watch Full', url=f'https://www.youtube.com/watch?v={v_id}&t={600}')],
            [InlineKeyboardButton(text='❌ Delete', callback_data='del')]
        ]
        v_data = get_vid_data(v_id=v_id)
        if not v_data:
            return False
        dl_thumb(url_=v_data['t_url'])
        dl_vid(v_url=v_data['v_url'])
        ffmpeg_extract_subclip(filename=f_path, t1=0, t2=600, targetname=cl_path)
        caption = v_data['title'] + '\n\n' + v_data['desc']
        if not v_data['broken']:
            keyboard.pop(0)

        context.bot.send_video(
            timeout=30,
            chat_id='399835396',
            video=open(cl_path, 'rb'),
            caption=caption,
            supports_streaming=True,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard),
            thumb=open(t_path, 'rb')
        )
        shutil.rmtree('./Temp')
        os.mkdir('./Temp')

        return True

    except Exception as exp:

        logger.exception(exp)

        return False
