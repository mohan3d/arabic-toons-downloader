#!/usr/bin/env python
# coding: utf-8
"""
arabic-toons-downloader - API-less arabic-toons movies and series downloader

Usage:
    downloader.py movie <movie_url> [<directory>]
    downloader.py episode <episode_url> [<directory>]
    downloader.py series <series_url> [<directory>] [options]
    downloader.py (-h | --help | --version | --usage)

Options:
    -e EPISODES, --episodes EPISODES        Maximum number of new files to download
                                            EPISODES must be in format "2 5 3-7"
    -h, --help                              Display this message and quit
    --version                               Show program version and quit
"""
import os
import re
import sys

import bs4
import docopt
import librtmp
import requests

__author__ = "mohan3d"
__author_email__ = "mohan3d94@gmail.com"
__version__ = "0.1.0"


class PageParser:
    def __init__(self):
        self.session = requests.session()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0"
        self.session.headers.update({
            'User-Agent': self.user_agent,
            'Accept': 'text/html',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Host': 'www.arabic-toons.com',
        })

    def _html(self, url):
        return self.session.get(url).content.decode()

    def _parse(self, html):
        raise NotImplementedError()


class VideoParser(PageParser):
    _RX_PAGE_DATA = re.compile(r"document\.write\(unescape\('([^']+)'\)\);")
    _RX_STREAM_URL = re.compile(r'url: "(rtmp://[^"]+)"')

    def _parse(self, html):
        page_data = requests.utils.unquote(self._RX_PAGE_DATA.search(html).group(1))
        stream_url = self._RX_STREAM_URL.search(page_data)
        return stream_url.group(1)

    def get_stream_url(self, url):
        html = self._html(url)
        return self._parse(html)


class SeriesParser(PageParser):
    def _parse(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        series_table = soup.find('table')

        return [td.find('a')['href'] for td in series_table.find_all('td')]

    def get_episodes_urls(self, url):
        html = self._html(url)
        return self._parse(html)


class VideoDownloader:
    def __init__(self, video_url):
        self.url = video_url
        self.conn = librtmp.RTMP(self.url, live=True)

    def download(self, directory):
        self.conn.connect()
        stream = self.conn.create_stream()

        with open(os.path.join(directory, self._get_file_name()), 'wb') as f:
            for data in stream:
                f.write(data)

    def _get_file_name(self, ext='flv'):
        return "{0}.{1}".format(self.url.split('/')[-1].split('.')[0], ext)


class ATDownloader:
    def __init__(self, directory):
        self.directory = directory

        if self.directory is not None and not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _download_video(self, url):
        stream_url = VideoParser().get_stream_url(url)
        VideoDownloader(stream_url).download(self.directory)

    def download_movie(self, movie_url):
        self._download_video(movie_url)

    def download_series(self, series_url, specific_episodes=None):
        episodes_urls = SeriesParser().get_episodes_urls(series_url)

        if specific_episodes:
            parsed_episodes = self._parse_episodes(specific_episodes)
            episodes_urls = [url for i, url in enumerate(episodes_urls, 1)
                             if i in parsed_episodes]

        for episode_url in episodes_urls:
            self._download_video(episode_url)

    def _parse_episodes(self, episodes_str):
        for episodes_range in episodes_str.split():
            p = episodes_range.split('-')

            start = end = p[0]
            end = p[1] if len(p) == 2 else end

            for episode in range(int(start), int(end) + 1):
                yield episode


def main(argv=sys.argv[1:]):
    args = docopt.docopt(__doc__, argv, version='arabic-toons-downloader {}'.format(__version__))

    downloader = ATDownloader(directory=os.path.expanduser(args.get('<directory>') or os.getcwd()))

    try:
        if args.get('movie'):
            downloader.download_movie(args.get('<movie_url>'))
        elif args.get('episode'):
            downloader.download_movie(args.get('<episode_url>'))
        elif args.get('series'):
            downloader.download_series(args.get('<series_url>'),
                                       specific_episodes=args.get('--episodes'))
    except:
        # Temporary
        pass


if __name__ == "__main__":
    main()
