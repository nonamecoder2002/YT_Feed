import asyncio

from Modules.Classes import Key

from Modules.yt_api import (
    make_video_pool,
    compare,
    get_video_details,
    make_message_content
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
    {'channelId': 'UCEC4D0dTTJr_EEnEJz15hnQ', 'channelTitle': '24 Канал'}
]

perm_video_pool = [

]

latest_pool = [

]
make_video_pool(channel_pool_=channel_pool, video_pool_=perm_video_pool, api_keys=api_keys)


async def main():
    print('--------------------------')
    while True:
        await asyncio.sleep(delay=300)
        global latest_pool, perm_video_pool
        temp_video_pool = []
        make_video_pool(channel_pool_=channel_pool, video_pool_=temp_video_pool, api_keys=api_keys)
        print('Temp pool: ', temp_video_pool)
        compare(old_pool=perm_video_pool, new_pool=temp_video_pool, output_pool=latest_pool)
        if latest_pool:
            perm_video_pool = temp_video_pool
            for video in latest_pool:
                video_details = get_video_details(api_keys_=api_keys, video_id=video['videoId'])
                print(make_message_content(response_item_=video_details), '\n')
        latest_pool = []
        print('--------------------------')


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task = [
        loop.create_task(main()),
            ]
    loop.run_until_complete(asyncio.wait(task))
