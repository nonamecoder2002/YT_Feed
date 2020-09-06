import logging

import os

from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler
)

from TG.ptb_funcs import (
    send_video,
    del_mes
)

from YT.yt_api import (
    fetch_uploads,
    fetch_lat
)

from YT.Classes import Key

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s-->%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs.txt', mode='w')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

if not os.path.exists('./Temp'):
    os.mkdir(path='./Temp')

api_keys = [
    Key(value='AIzaSyBTZ9drxqXKkh8yijdYaBQS1ijANQQApZQ'),
    Key(value='AIzaSyBtNGfLBehI11PeOeInuyXviPWTE3tglrM')
]

channel_pool = [
    {'channelId': 'UCg0bIYJXvberMBRdO1k1Dxg', 'channelTitle': 'Izzy ᴸᴬᴵᶠ'},
    {'channelId': 'UC1qWaT8_iPHSBYgB4T2ltuA', 'channelTitle': 'Ай, Как Просто!'},
    {'channelId': 'UCq7JZ8ATgQWeu6sDM1czjhg', 'channelTitle': 'StopGame.Ru'},
    {'channelId': 'UCspfe9lef7ApJaHQsOcPC1A', 'channelTitle': 'overbafer1'},
    {'channelId': 'UCQWeDEwQruA_CcyR08bIE9g', 'channelTitle': 'iKakProsto2'},
    {'channelId': 'UCY03gpyR__MuJtBpoSyIGnw', 'channelTitle': 'Droider.Ru'},
    {'channelId': 'UCyoLK278J8j5e4MpMT5WOyg', 'channelTitle': 'Slava Gorbatenko'},
    {'channelId': 'UC6uFoHcr_EEK6DgCS-LeTNA', 'channelTitle': 'PRO Hi-Tech'},
    {'channelId': 'UCWVGUI2haKuZiJiInenVP6A', 'channelTitle': 'ВЄСТІ'},
    {'channelId': 'UCrzwOa2lzzPjfiLIn7Y8SrQ', 'channelTitle': 'Кик Обзор'},
    {'channelId': 'UCF_ZiWz2Vcq1o5u5i1TT3Kw', 'channelTitle': 'Телебачення Торонто'},
    {'channelId': 'UCntek4Y39faSPt0SxzJkb9A', 'channelTitle': 'The King Drive'},


]

uploads = []


def vid_feed(context: CallbackContext):

    global uploads

    for _channel in channel_pool:
        v_id = fetch_lat(channel_id=_channel['channelId'], keys=api_keys)

        if v_id not in uploads:

            try:
                logger.info(f'Fetched Video: {v_id}')
                send_video(
                    context=context,
                    v_id=v_id,
                    f_path_='./Temp/video.mp4',
                    clip_path='./Temp/clip.mp4'
                )
                logger.info(f'Sent Video {v_id}')
                uploads.append(v_id)

            except Exception as exp:
                
                logger.exception(exp)

def send_logs(update, context):

    if update.effective_user.id == 399835396:

        update.message.reply_document(
           open('logs.txt', 'rb')
        )
        del_mes(_update=update, _context=context)


def call_handler(update, context):

    call = update.callback_query

    if call.data == 'del':
        del_mes(_update=call, _context=context)


def get_uploads(context: CallbackContext):

    global uploads, channel_pool
    uploads.clear()

    for channel in channel_pool:

        fetch_uploads(
            channel_id=channel['channelId'],
            keys=api_keys,
            out=uploads
        )


def main():

    updater = Updater(
        token='1254645903:AAGK9Lud_wRONgINQMm6xgeroQmA89zSC5I',
        use_context=True
                      )
    job = updater.job_queue

    job.run_repeating(callback=get_uploads, interval=86400, first=0)

    job.run_repeating(callback=vid_feed, interval=200, first=0)

    _dispatcher = updater.dispatcher

    _dispatcher.add_handler(CommandHandler('logs', send_logs))

    _dispatcher.add_handler(CallbackQueryHandler(callback=call_handler))

    updater.start_polling()

    logger.info('Bot is up')

    updater.idle()


if __name__ == '__main__':
    main()
