from glob import glob
import os

from xml.etree import ElementTree as ET
import re


def convert(lrc_path):

    with open(lrc_path, 'r', encoding='utf-8') as file:
        content = file.read()


    # 解析TTML文件
    tree = ET.fromstring(content)
    namespaces = {'ttml': 'http://www.w3.org/ns/ttml'}  # 定义命名空间

    # 提取时间和歌词
    lyrics = []
    for p in tree.findall('.//ttml:p', namespaces):
        begin = p.get('begin')
        end = p.get('end')
        text = ''.join(p.itertext())

        # 将时间格式转换为LRC格式
        begin_time = re.sub(r'(\d+):(\d+):(\d+)\.(\d+)', r'[\1:\2.\3]', begin)
        # 只需要开始时间来同步歌词，结束时间在LRC格式中不使用

        # 构建LRC行
        lyrics.append(f'{begin_time} {text}')

    # 合并为LRC格式字符串
    # 调整格式：在时间戳前添加空格，确保时间戳和歌词之间有一个空格
    lyrics_formatted = []
    for line in lyrics:
        # 分割时间戳和歌词
        time, text = line.split(' ', 1)
        # 调整格式
        formatted_line = f'[{time}] {text}'
        lyrics_formatted.append(formatted_line)

    # 重新合并为LRC格式字符串
    lrc_content_formatted = '\n'.join(lyrics_formatted)
    return lrc_content_formatted


if not os.path.exists('../lrclib'):
    os.makedirs('../lrclib')

ttml_files = glob('../lyrics/*.ttml')
for ttml_file in ttml_files:
    lrc_content = convert(ttml_file)
    lrc_file = '../lrclib/' + os.path.basename(ttml_file).replace('.ttml', '.lrc')
    with open(lrc_file, 'w', encoding='utf-8') as file:
        file.write(lrc_content)