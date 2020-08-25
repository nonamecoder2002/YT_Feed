from telegram.ext import Updater, CallbackContext

import datetime

from YT.yt_api import (
    locator,
    latest_vid_id
)


from YT.Classes import Key

from YT.pyTube import (
    downloader,
    get_vid_data
)

from io import BytesIO

api_keys = [
    Key(value='AIzaSyBTZ9drxqXKkh8yijdYaBQS1ijANQQApZQ'),
    Key(value='AIzaSyBtNGfLBehI11PeOeInuyXviPWTE3tglrM')
]

channel_pool = [
    # {'channelId': 'UCGBFIBxDuaEmrL5CxXSxx6g', 'channelTitle': 'СТАС'},
    # {'channelId': 'UCg0bIYJXvberMBRdO1k1Dxg', 'channelTitle': 'Izzy ᴸᴬᴵᶠ'},
    # {'channelId': 'UC1qWaT8_iPHSBYgB4T2ltuA', 'channelTitle': 'Ай, Как Просто!'},
    # {'channelId': 'UCq7JZ8ATgQWeu6sDM1czjhg', 'channelTitle': 'StopGame.Ru'},
    # {'channelId': 'UCspfe9lef7ApJaHQsOcPC1A', 'channelTitle': 'overbafer1'},
    # {'channelId': 'UCQWeDEwQruA_CcyR08bIE9g', 'channelTitle': 'iKakProsto2'},
    {'channelId': 'UCrp_UI8XtuYfpiqluWLD7Lw', 'channelTitle': 'CNBC Television'},
    {'channelId': 'UCEC4D0dTTJr_EEnEJz15hnQ', 'channelTitle': '24 Канал'},
    {'channelId': 'UCupvZG-5ko_eiXAupbDfxWw', 'channelTitle': 'CNN'},
    {'channelId': 'UCeY0bbntWzzVIaj2z3QigXg', 'channelTitle': 'NBCNews'}
]

perm_video_pool = []


for channel in channel_pool:
    latest_v_id = latest_vid_id(channel_id=channel['channelId'], keys=api_keys)
    perm_video_pool.append(latest_v_id)


def vid_feed(context: CallbackContext):
    global perm_video_pool
    print(datetime.datetime.now())
    located = locator(
        channel_pool=channel_pool,
        perm_video_pool=perm_video_pool,
        api_keys=api_keys
    )
    latest_v_pool = located[0]
    temp_pool = located[1]
    print(temp_pool)
    for video_id in latest_v_pool:
        stream = BytesIO()
        print('Sending: ', video_id)
        v_data = get_vid_data(v_id=video_id)
        downloader(i_stream=stream, v_url=v_data['v_url'])
        stream.seek(0)
        caption = v_data['title'] + '\n\n' + v_data['desc']
        context.bot.send_video(
            chat_id='399835396',
            video=stream,
            caption=caption,
            height=720,
            width=1280,
            supports_streaming=True
        )
        stream.close()
    perm_video_pool = temp_pool


def main():

    updater = Updater(
        token='1254645903:AAGK9Lud_wRONgINQMm6xgeroQmA89zSC5I',
        use_context=True
                      )
    job = updater.job_queue

    job.run_repeating(vid_feed, interval=120, first=0)

    _dispatcher = updater.dispatcher

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
