import logging
import sys
import re
from io import BytesIO
from urllib.parse import urljoin

import requests
from mutagen.mp3 import MP3
from lxml.etree import HTML
from rich.logging import RichHandler


def get_logger(logger_name, log_file_path="runtime.log"):
	# 格式化器
	fmt = "'%(asctime)s [%(name)s] %(levelname)s: %(message)s'"
	formatter = logging.Formatter(fmt)

	# 处理器 - 决定日志流向
	fh = logging.FileHandler(filename=log_file_path, encoding="utf8")
	# sh = logging.StreamHandler(stream=sys.stdout)
	sh = RichHandler()
	# 格式化器配备在处理器上
	fh.setFormatter(formatter)
	sh.setFormatter(formatter)

	# 创建一个 logger
	logger = logging.getLogger(name=logger_name)
	logger.setLevel(logging.DEBUG)
	logger.addHandler(fh)
	logger.addHandler(sh)

	return logger


def extract_rank_list(home_url="http://www.5nd.com/paihang/"):
	"""
	
	@return: [("好听的歌", "http://www.5nd.com/paihang/tuijiangequ.htm"), ...]
	"""

	response = HTML(requests.get(home_url).content.decode("gbk"))

	url_list = response.xpath("//ul[@class='rankListOne']//li/a/@href")
	name_list = response.xpath("//ul[@class='rankListOne']//li/a/text()")

	url_list = map(
		lambda u: urljoin(home_url, u), url_list
	)

	return zip(name_list, url_list)


def extract_music_list(url):
	"""

	@return: [("到了这个年纪 - 赵阿光", "http://www.5nd.com/ting/665026.html"), ...]
	"""

	response = HTML(requests.get(url).content.decode("gbk"))

	url_list = response.xpath("//ul[contains(@id, 'pl')]/li/a/@href")
	name_list = response.xpath("//ul[contains(@id, 'pl')]/li/a/text()")

	url_list = map(
		lambda u: urljoin(url, u), url_list
	)

	return zip(name_list, url_list)


def extract_music_info(url):
	response = HTML(requests.get(url).content.decode("gbk"))

	publish_time = response.xpath("//div[@class='songInfo']//li[contains(text(), '发行时间')]/text()")[0]
	publish_time = re.search(r"(\d+-?)+", publish_time).group(0)

	mp3_content = requests.get(
		urljoin("http://mpge.5nd.com/", response.xpath("//div[@id='kuPlayer']/@data-play")[0])
	).content
	duration = int(MP3(BytesIO(mp3_content)).info.length)

	return {
		"name": response.xpath("//div[@class='songAboutL']/h1/a/text()")[0],
		"singer_name": response.xpath("//div[@class='songInfo']//a[@target='_singer']/text()")[0],
		"album": response.xpath("//div[@class='songInfo']//a[@target='_album']/text()")[0],
		"publish_time": publish_time,
		"lyric": "\n".join(response.xpath("//div[@class='songLyricCon']/p//text()")),
		"duration": duration,
	}

