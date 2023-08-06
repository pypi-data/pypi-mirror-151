import requests
from lxml import etree
import pandas as pd
import re

def response(url):
    headers = {
        'user-agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.55'
    }
    res = requests.get(url=url, headers=headers)
    res.encoding = 'utf-8'
    return res

def check(msg_list):
    for num in range(len(msg_list)):
        msg_list[num] = msg_list[num].replace(' ','').replace('\n','')
    return msg_list

def get_tag(aid):
    url = 'https://api.bilibili.com/x/web-interface/view/detail/tag?aid={}'.format(aid)
    res = response(url)
    pattern = r'"tag_name":"(.*?)"'
    tags = re.findall(pattern, res.text)
    return ','.join(tags)

def get_msg(res):
    page_text = res.content
    tree = etree.HTML(page_text)
    video_list = tree.xpath('//*[@id="app"]/div/div[2]/div[2]/ul')
    for li in video_list:
        video_name = li.xpath('./li/div/div/a/text()')
        video_play = li.xpath('./li/div/div[2]/div/div/span[1]/text()')
        video_artists = li.xpath('./li/div/div[2]/div/a/span/text()')
        video_aid = li.xpath('./li/@data-id')
    for i in (video_name,video_play,video_artists):
        check(i)
    video_tag = []
    for aid in video_aid:
        video_tag.append(get_tag(aid))
    msg = {'Video_Name':video_name,"Video_Play":video_play,"Video_artists":video_artists,"Video_tag":video_tag}
    df = pd.DataFrame(msg)
    return df

def get_b_rank():
    url = 'https://www.bilibili.com/v/popular/rank/all'
    res = response(url)
    df = get_msg(res)
    return df