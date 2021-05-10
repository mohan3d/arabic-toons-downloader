# !/usr/bin/env python
# coding: utf-8
"""
arabic-toons-downloader - API-less arabic-toons movies and series downloader

Usage:
    downloader.py movie <movie_url> [<directory>]
    downloader.py episode <episode_url> [<directory>]
    downloader.py series <series_url> [<directory>] [options]
    downloader.py (-h | --help | --version | --usage)

Options:
    -e EPISODES, --episodes EPISODES        Maximum number of new files
                                            to download EPISODES must be
                                            in format "2 5 3-7"
    -h, --help                              Display this message and quit
    --version                               Show program version and quit
"""
import concurrent.futures
import os
import re
import subprocess
import sys

import bs4
import docopt
import m3u8
import requests

__author__ = "mohan3d"
__author_email__ = "mohan3d94@gmail.com"
__version__ = "0.1.3"

ARABIC_TOONS_HOST = 'www.arabic-toons.com'
ARABIC_TOONS_USER_AGENT = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/90.0.4430.93 Safari/537.36 '
}


class PageParser:
    def __init__(self):
        self.session = requests.session()
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) " \
                          "Gecko/20100101 Firefox/50.0"

        self.session.headers.update({
            **ARABIC_TOONS_USER_AGENT,
            'Accept': 'text/html',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Host': ARABIC_TOONS_HOST,
        })

    def _html(self, url):
        return self.session.get(url).content.decode('utf-8')

    def _parse(self, html):
        raise NotImplementedError()


class VideoParser(PageParser):
    _RX_PAGE_DATA = re.compile(r"document\.write\(unescape\('([^']+)'\)\);")
    _RX_STREAM_URL = re.compile(r'<source src="(http://[^"]+)" type="application/x-mpegURL">')

    def _parse(self, html):
        return requests.utils.unquote(self._RX_STREAM_URL.search(html).group(1))

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


class StreamDownloader:
    def __init__(self, stream_url: str, filepath: str, workers: int = 16, ffmpeg: bool = False):
        self.url = stream_url
        self.path = filepath
        self.workers = workers
        self.ffmpeg = ffmpeg

        self.session = requests.session()
        self.session.headers.update(ARABIC_TOONS_USER_AGENT)

    def download(self, directory: str):
        segments = self._get_segments()
        filepath = os.path.join(directory, self.path) + '.ts'

        if self.workers and self.workers > 1:
            with concurrent.futures.ProcessPoolExecutor(max_workers=self.workers) as executor:
                responses = executor.map(self.session.get, segments)
        else:
            responses = [self.session.get(segment_url) for segment_url in segments]

        with open(filepath, 'wb') as f:
            for response in responses:
                f.write(response.content)

        if self.ffmpeg:
            self._ffmpeg(filepath)

    def _get_segments(self):
        return m3u8.load(self.url, headers=self.session.headers).segments.uri

    @staticmethod
    def _ffmpeg(path: str):
        output_path = path.replace('.ts', '.mp4')
        subprocess.run(["ffmpeg", "-i", path, "-acodec", "copy", "-vcodec", "copy", output_path])


class ATDownloader:
    def __init__(self, directory):
        self.directory = directory

        if self.directory is not None and not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _download_video(self, url):
        stream_url = VideoParser().get_stream_url(url)
        filepath = self._get_file_name(url)
        StreamDownloader(stream_url, filepath).download(self.directory)

    def download_movie(self, movie_url):
        self._download_video(movie_url)

    def download_series(self, series_url, specific_episodes=None):
        episodes_urls = SeriesParser().get_episodes_urls(series_url)

        if specific_episodes:
            parsed_episodes = list(self._parse_episodes(specific_episodes))
            episodes_urls = [url for i, url in enumerate(episodes_urls, 1)
                             if i in parsed_episodes]

        for episode_url in episodes_urls:
            self._download_video(episode_url)

    @staticmethod
    def _parse_episodes(episodes_str):
        for episodes_range in episodes_str.split():
            p = episodes_range.split('-')

            start = end = p[0]
            end = p[1] if len(p) == 2 else end

            for episode in range(int(start), int(end) + 1):
                yield episode

    @staticmethod
    def _get_file_name(url):
        return url.split('/')[-1].split('?')[0]


def main():
    args = docopt.docopt(__doc__, argv=sys.argv[1:], version=__version__)

    downloader = ATDownloader(
        directory=os.path.expanduser(args.get('<directory>') or os.getcwd()))

    try:
        if args.get('movie'):
            downloader.download_movie(args.get('<movie_url>'))
        elif args.get('episode'):
            downloader.download_movie(args.get('<episode_url>'))
        elif args.get('series'):
            downloader.download_series(args.get('<series_url>'),
                                       args.get('--episodes'))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
