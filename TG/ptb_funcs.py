import os

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
        update.message.reply_document(
            open('./Temp/logs.txt', 'rb')
        )
        del_mes(_update=update, _context=context)


def call_handler(update, context):
    call = update.callback_query

    if call.data == 'del':
        del_mes(_update=call, _context=context)


def mk_thumb(context):
    blank = Image.new(
        mode='1',
        size=(1280, 720),
        color=None
    )
    blank.thumbnail(
        (320, 320)
    )

    blank.save(fp='./Temp/blank.jpg')


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


def send_video(context, v_id: str):
    try:
        f_path_ = './Temp/video.mp4'
        clip_path = './Temp/clip.mp4'
        keyboard = [[InlineKeyboardButton(text='❌ Delete', callback_data='del')]]
        v_data = get_vid_data(v_id=v_id)
        if not v_data:
            return False
        dl_vid(file_path=f_path_, v_url=v_data['v_url'])
        ffmpeg_extract_subclip(filename=f_path_, t1=0, t2=700, targetname=clip_path)
        os.remove(f_path_)
        caption = v_data['title'] + '\n\n' + v_data['desc']
        if v_data['broken']:
            keyboard.insert(0,
                            [InlineKeyboardButton(text='📺 Watch Full',
                                                  url=f'https://www.youtube.com/watch?v={v_id}&t={700}')]
                            )
        markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_video(
            timeout=30,
            chat_id='399835396',
            video=open(clip_path, 'rb'),
            caption=caption,
            supports_streaming=True,
            parse_mode='HTML',
            reply_markup=markup,
            thumb=open('./Temp/blank.jpg', 'rb')
        )
        os.remove(clip_path)

        return True

    except Exception as exp:

        logger.exception(exp)

        return False
