import asyncio

from YT.Classes import Key

from YT.yt_api import (
    latest_vid_id,
    compare
)
from YT.pyTube import (
    get_vid_url,
    get_vid_thumbnail,
    get_vid_info
)

api_keys = [
    Key(value='AIzaSyBTZ9drxqXKkh8yijdYaBQS1ijANQQApZQ'),
    Key(value='AIzaSyBtNGfLBehI11PeOeInuyXviPWTE3tglrM')
]

channel_pool = [
    # {'channelId': 'UCGBFIBxDuaEmrL5CxXSxx6g', 'channelTitle': 'СТАС'},
    # {'channelId': 'UCptRK95GEDXvJGOQIFg50fg', 'channelTitle': 'Игорь Линк'},
    # {'channelId': 'UC9MK8SybZcrHR3CUV4NMy2g', 'channelTitle': 'Диджитализируй!'},
    # {'channelId': 'UCPIKvg4P2pRDdmyN1gi9bnA', 'channelTitle': 'MovieMaker'},
    # {'channelId': 'UCg0bIYJXvberMBRdO1k1Dxg', 'channelTitle': 'Izzy ᴸᴬᴵᶠ'},
    # {'channelId': 'UC1qWaT8_iPHSBYgB4T2ltuA', 'channelTitle': 'Ай, Как Просто!'},
    # {'channelId': 'UCCezIgC97PvUuR4_gbFUs5g', 'channelTitle': 'Corey Schafer'},
    # {'channelId': 'UCq7JZ8ATgQWeu6sDM1czjhg', 'channelTitle': 'StopGame.Ru'},
    # {'channelId': 'UC9DXAsBD4-ITVuvpd68401Q', 'channelTitle': 'AutoTopNL'},
    # {'channelId': 'UCspfe9lef7ApJaHQsOcPC1A', 'channelTitle': 'overbafer1'},
    {'channelId': 'UCEC4D0dTTJr_EEnEJz15hnQ', 'channelTitle': '24 Канал'},
    {'channelId': 'UCrp_UI8XtuYfpiqluWLD7Lw', 'channelTitle': 'CNBCtelevision'},
]

perm_video_pool = []

for channel in channel_pool:
    latest_v_id = latest_vid_id(channel_id=channel['channelId'], keys=api_keys)
    perm_video_pool.append(latest_v_id)


async def main():
    while True:
        global perm_video_pool
        temp_video_pool, latest_video_pool = [], []
        for _channel in channel_pool:
            _latest_v_id = latest_vid_id(channel_id=_channel['channelId'], keys=api_keys)
            temp_video_pool.append(_latest_v_id)
        print('temp_video_pool: ', temp_video_pool, '\n')
        compare(old_pool=perm_video_pool, new_pool=temp_video_pool, output_pool=latest_video_pool)
        perm_video_pool = temp_video_pool
        for video_id in latest_video_pool:
            video = get_vid_url(vid_id=video_id)
            preview = get_vid_thumbnail(vid_id=video_id)
            description = get_vid_info(vid_id=video_id)
            print('Got New video {} \n {}\n {}'.format(video, preview, description))
        print('***************')
        await asyncio.sleep(delay=100)

if __name__ == '__main__':
    asyncio.run(main())
