import asyncio

from Modules.Classes import Key, KeyExpired

from Modules.yt_api import (
    make_video_pool,
    update_video_pool,
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
    {'channelId': 'UC1qWaT8_iPHSBYgB4T2ltuA', 'channelTitle': 'Ай, Как Просто!'},
    {'channelId': 'UCCezIgC97PvUuR4_gbFUs5g', 'channelTitle': 'Corey Schafer'},
    {'channelId': 'UCq7JZ8ATgQWeu6sDM1czjhg', 'channelTitle': 'StopGame.Ru'},
    # {'channelId': 'UC9DXAsBD4-ITVuvpd68401Q', 'channelTitle': 'AutoTopNL'},
    # {'channelId': 'UCspfe9lef7ApJaHQsOcPC1A', 'channelTitle': 'overbafer1'}
]

video_pool = [

]

latest_pool = [

]
make_video_pool(channel_pool_=channel_pool, video_pool_=video_pool, api_keys=api_keys)

print(video_pool)
