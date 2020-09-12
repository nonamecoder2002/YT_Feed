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


def send_logs(update, context):
    if update.effective_user.id == 399835396:
        keyboard = [[InlineKeyboardButton(text='❌ Delete', callback_data='del')]]
        context.bot.send_document(
            chat_id=update.effective_user.id,
            document=open('./logs.txt', 'rb'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        del_mes(_update=update, _context=context)


def call_handler(update, context):
    call = update.callback_query

    if call.data == 'del':
        del_mes(_update=call, _context=context)


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
    try:
        keyboard = [
            [InlineKeyboardButton(text='📺 Watch Full', url=f'https://www.youtube.com/watch?v={v_id}&t={700}')],
            [InlineKeyboardButton(text='❌ Delete', callback_data='del')]
        ]
        v_data = get_vid_data(v_id=v_id)
        if not v_data:
            return False
        dl_thumb(url_=v_data['t_url'])
        dl_vid(v_url=v_data['v_url'])
        ffmpeg_extract_subclip(filename='./Temp/video.mp4', t1=0, t2=700, targetname='./Temp/clip.mp4')
        caption = v_data['title'] + '\n\n' + v_data['desc']
        if not v_data['broken']:
            keyboard.pop(0)

        context.bot.send_video(
            timeout=30,
            chat_id='399835396',
            video=open('./Temp/clip.mp4', 'rb'),
            caption=caption,
            supports_streaming=True,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard),
            thumb=open('./Temp/thumb.jpg', 'rb')
        )
        shutil.rmtree('./Temp')
        os.mkdir('./Temp')

        return True

    except Exception as exp:

        logger.exception(exp)

        return False
