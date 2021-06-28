import json
import csv
from urllib.parse import urljoin

import requests
from lxml.etree import HTML
from util import *
from rich.pretty import pretty_repr


logger = get_logger("crawl.py")


def crawl():
	for category_name, url in extract_rank_list():
		logger.info("当前类别: {}({})".format(category_name, url))
		for music_name, music_detail_url in extract_music_list(url):
			logger.info("抓取音乐: {}({})".format(music_name, music_detail_url))
			
			try:
				item = extract_music_info(music_detail_url)
			except Exception as e:
				logger.debug(
					"提取音乐元信息时({})，发生异常: \n".format(music_detail_url)
				)
				logger.debug(str(e))
			else:
				yield {
					**item,
					"category": category_name,
				}

def main():
	with open("items.csv", "a") as f:
		csv_w = csv.DictWriter(f, ["name", "singer_name", "album", "publish_time", "lyric", "duration", "category"])
		for item in crawl():
			logger.debug("成功获取: {}".format(pretty_repr(item)))
			csv_w.writerow(item)


if __name__ == "__main__":
	main()