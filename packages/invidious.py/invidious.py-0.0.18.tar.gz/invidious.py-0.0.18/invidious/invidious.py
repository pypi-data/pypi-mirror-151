from .playlist_item import PlaylistItem
from .channel_item import ChannelItem
from .recommended_video import RecommendedVideo
from .short_video import ShortVideo
from .video_item import VideoItem
from .channel import Channel
from .video import Video
from .config import *
import requests

WORKING_MIRRORS = []
LOGGING = True

def update_mirrors():
    WORKING_MIRRORS.clear()
    for mirror in MIRRORS:
        response = requests.get(mirror, headers=HEADERS)
        if response.status_code == 200:
            if LOGGING: print(f"Mirror {mirror} is work.")
            WORKING_MIRRORS.append(mirror)
            return
        else:
            if LOGGING: print(f"Mirror {mirror} doesn't work.")

def get_working_mirror():
    if len(WORKING_MIRRORS) == 0: update_mirrors()
    return WORKING_MIRRORS[0]

def request(url: str):
    mirror = get_working_mirror()
    response = requests.get(mirror+url, headers=HEADERS)
    if response.status_code == 200: return response.json()
    elif response.status_code == 429 and LOGGING: print("RequestError: Too many requests.")
    elif response.status_code == 404 and LOGGING: print("RequestError: Page not found.")

def search(query: str, page=0, sort_by="", duration="", date="", ctype="", feauters=[], region=""):
    """
    Invidious search method. Return list with VideoItem, ChannelItem, PlaylistItem.

    query: your search query.
    page: number of page.
    sort_by: [relevance, rating, upload_date, view_count].
    date: [hour, today, week, month, year].
    duration: [short, long].
    ctype: [video, playlist, channel, all] (default: video).
    feauters: [hd, subtitles, creative_commons, 3d, live, purchased, 4k, 360, location, hdr].
    region: ISO 3166 country code (default: US).
    """
    req = f"/api/v1/search?q={query}"
    if page > 0: req += f"&page={page}"
    if sort_by != "": req += f"&sort_by={sort_by}"
    if duration != "": req += f"&duration={duration}"
    if date != "": req += f"&date={date}"
    if ctype != "": req += f"&type={ctype}"
    if feauters != []:
        req += "&feauters="
        for feauter in feauters:
            req += feauter+","
        req = req[:len(req)-2]
    if region != "": req += f"region={region}"

    jdict = request(req)
    itemsList = []

    for item in jdict:
        citem = None
        if item['type'] == 'channel': citem = ChannelItem()
        elif item['type'] == 'video': citem = VideoItem()
        elif item['type'] == 'playlist': citem = PlaylistItem()
        if citem != None: 
            citem.loadFromDict(item)
            itemsList.append(citem)
    
    return itemsList

def get_video(videoId: str, region=""):
    """
    Invidious get_video method. Return Video by id.
    
    videoId: id of video.
    region: ISO 3166 country code (default: US).
    """
    req = f"/api/v1/videos/{videoId}"
    if region != "": req += f"?region={region}"

    response = request(req)
    if response == None: return None
        
    rVideos = response['recommendedVideos']
    recommendedVideos = []
    for item in rVideos:
        vitem = RecommendedVideo()
        vitem.loadFromDict(item)
        recommendedVideos.append(vitem)
    response['recommendedVideos'] = recommendedVideos

    video = Video()
    video.loadFromDict(response)

    return video

def get_channel(authorId: str, sort_by=""):
    """
    Invidious get_channel method. Return Channel by id.
    
    authorId: id of channel.
    sort_by: sorting channel videos. [newest, oldest, popular] (default: newest).
    """
    req = f"/api/v1/channels/{authorId}"
    if sort_by != "": req += f"?sort_by={sort_by}"

    response = request(req)
    if response == None: return None

    lVideos = response['latestVideos']
    latestVideos = []
    for item in lVideos:
        vitem = VideoItem()
        vitem.loadFromDict(item)
        latestVideos.append(vitem)
    response['latestVideos'] = latestVideos

    channel = Channel()
    channel.loadFromDict(response)

    return channel

def get_popular():
    """
    Invidious get_popular method. Return list with ShortVideo.
    """
    req = f"/api/v1/popular"

    response = request(req)
    if response == None: return None
        
    pVideos = response
    popularVideos = []
    for item in pVideos:
        vitem = ShortVideo()
        vitem.loadFromDict(item)
        popularVideos.append(vitem)

    return popularVideos

def get_trending(type="", region=""):
    """
    Invidious get_popular method. Return list with VideoItem.

    type: [music, gaming, news, movies].
    region: ISO 3166 country code (default: US).
    """
    req = f"/api/v1/trending"
    if type != "": req += f"?type={type}"
    if region != "" and type == "": req += f"?region={region}"
    elif region != "": req += f"&region={region}"

    response = request(req)
    if response == None: return None
        
    tVideos = response
    trendingVideos = []
    for item in tVideos:
        vitem = VideoItem()
        vitem.loadFromDict(item)
        trendingVideos.append(vitem)

    return trendingVideos

if __name__ == "__main__":
    print(get_channel("UCrPw1-nDPppBuh7UCBqu3GQ").author)
    print(get_video("L8Ohygt5UVY").title)
    items = search(query="kuplinov", date="today")
    for item in items:
        if type(item) == VideoItem:
            print(item.title)
