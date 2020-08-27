import logging

from telegram.ext import Updater, CallbackContext, CommandHandler

from TG.ptb_funcs import send_video

from YT.yt_api import (
    locator,
    latest_vid_id
)

from YT.Classes import Key


logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(levelname)s-->%(asctime)s:%(name)s:%(message)s')

file_handler = logging.FileHandler('logs.log', mode='w')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


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
    {'channelId': 'UCEC4D0dTTJr_EEnEJz15hnQ', 'channelTitle': '24 Канал'},

]

perm_video_pool = []


for channel in channel_pool:
    latest_v_id = latest_vid_id(channel_id=channel['channelId'], keys=api_keys)
    perm_video_pool.append(latest_v_id)


def vid_feed(context: CallbackContext):
    global perm_video_pool
    located = locator(
        channel_pool=channel_pool,
        perm_video_pool=perm_video_pool,
        api_keys=api_keys
    )
    latest_v_pool, temp_pool = located
    logger.info(f'Temporary vid pool: {temp_pool}')
    for video_id in latest_v_pool:
        logger.info(f'Sending video: {video_id}')
        send_video(context=context, v_id=video_id)
    perm_video_pool = temp_pool


def send_logs(update, context):
    if update.effective_user.id == 399835396:
        update.message.reply_document(
           open('logs.log', 'rb')
        )


def main():

    updater = Updater(
        token='1254645903:AAGK9Lud_wRONgINQMm6xgeroQmA89zSC5I',
        use_context=True
                      )
    job = updater.job_queue

    job.run_repeating(vid_feed, interval=180, first=0)

    _dispatcher = updater.dispatcher

    _dispatcher.add_handler(CommandHandler('logs', send_logs))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
