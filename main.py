import logging

from telegram.ext import (
    Updater,
    CallbackContext,
    CommandHandler,
    CallbackQueryHandler
)

from TG.ptb_funcs import (
    send_video,
    mk_thumb,
    send_logs,
    call_handler
)

from YT.yt_api import (
    fetch_uploads,
    fetch_lat
)

from YT.Classes import Key

logging.basicConfig(
    filename='./Temp/logs.txt',
    level=logging.INFO,
    filemode='w',
    format='%(levelname)s-->%(asctime)s:|%(name)s|: %(message)s'

)

logger = logging.getLogger(__name__)

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
    {'channelId': 'UCIALMKvObZNtJ6AmdCLP7Lg', 'channelTitle': 'Bloomberg'}


]

uploads = []


def vid_feed(context: CallbackContext):

    global uploads

    for _channel in channel_pool:

        v_id = fetch_lat(channel_id=_channel['channelId'], keys=api_keys)

        if v_id not in uploads:

            logger.info(f'Fetched Video: {v_id}')

            if send_video(context=context, v_id=v_id):

                logger.info(f'Sent Video {v_id}')

                uploads.append(v_id)
            else:

                pass


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

    job.run_once(callback=mk_thumb, when=0)

    job.run_repeating(callback=get_uploads, interval=86400, first=1)

    job.run_repeating(callback=vid_feed, interval=200, first=2)

    _dispatcher = updater.dispatcher

    _dispatcher.add_handler(CommandHandler('logs', send_logs))

    _dispatcher.add_handler(CallbackQueryHandler(callback=call_handler))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
