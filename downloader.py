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
    -s SEGMENTS, --segments SEGMENTS        Number of segments to be downloaded in parallel,
                                            for faster network and cpu set to 16 or 32
    -p PROCESSES, --processes PROCESSES     Maximum number of processes to be used to download series
                                            for faster network and cpu set to 4 or 8
    --ffmpeg                                ffmpeg support will result "mp4" files,
                                            ffmpeg must be already installed in the system
                                            and accessible.
                                            (n episodes will be downloaded in parallel)
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

DEFAULT_SIMULTANEOUS_SEGMENTS_COUNT = 4
DEFAULT_PROCESSES_COUNT = 1


class PageParser:
    def __init__(self):
        self.session = requests.session()

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
    _STREAM_URL = re.compile(r'<source src="(http://[^"]+)" type="application/x-mpegURL">')
    _STREAM_TITLE = re.compile(r'<h1 style="padding:15px">([^<]+)</h1>')

    def _parse(self, html):
        return self._extract(html, self._STREAM_URL)

    def _parse_title(self, html):
        return self._extract(html, self._STREAM_TITLE)

    def get_stream_info(self, url):
        html = self._html(url)
        url = self._parse(html)
        title = self._parse_title(html)
        title = ' '.join(title.split(' ')[1:]).strip()

        return url, title

    @staticmethod
    def _extract(html: str, regex: re.Pattern):
        return requests.utils.unquote(regex.search(html).group(1))


class SeriesParser(PageParser):
    def _parse(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        series_list = soup.findAll('div', attrs={'class': 'col-sm-4 col-xs-6 col-md-2 col-lg-2'})

        return ['http://{}/{}'.format(ARABIC_TOONS_HOST, div.find('a')['href']) for div in series_list]

    def get_episodes_urls(self, url):
        html = self._html(url)
        return self._parse(html)


class StreamDownloader:
    def __init__(self, stream_url: str, workers: int = 1, ffmpeg: bool = False):
        self.url = stream_url
        self.workers = workers
        self.ffmpeg = ffmpeg

        self.session = requests.session()
        self.session.headers.update(ARABIC_TOONS_USER_AGENT)

    def download(self, filepath: str):
        mp4path = filepath.replace('.ts', '.mp4')

        if not os.path.exists(mp4path):
            if not os.path.exists(filepath):
                self._download(filepath)
            else:
                print(f'{filepath} already exists!')

            if self.ffmpeg:
                self._ffmpeg(filepath)
        else:
            print(f'{mp4path} already exists!')

    def _download(self, filepath):
        segments = self._get_segments()

        if self.workers and self.workers > 1:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
                responses = executor.map(self.session.get, segments)
        else:
            responses = [self.session.get(segment_url) for segment_url in segments]

        with open(filepath, 'wb') as f:
            for response in responses:
                f.write(response.content)

    def _get_segments(self):
        return m3u8.load(self.url, headers=self.session.headers).segments.uri

    @staticmethod
    def _ffmpeg(path: str, remove_input=True):
        output_path = path.replace('.ts', '.mp4')

        subprocess.run(["ffmpeg", "-i", path, "-acodec", "copy", "-vcodec", "copy", output_path],
                       stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=True)

        if remove_input:
            os.remove(path)


class ATDownloader:
    def __init__(self, directory, workers: int = 1, ffmpeg: bool = False):
        self.workers = workers
        self.ffmpeg = ffmpeg
        self.directory = directory

        if self.directory is not None and not os.path.exists(self.directory):
            os.makedirs(self.directory)

    def _download_video(self, url):
        stream_url, stream_title = VideoParser().get_stream_info(url)
        filepath = os.path.join(self.directory, self._get_file_name(stream_title))

        StreamDownloader(stream_url, workers=self.workers, ffmpeg=self.ffmpeg).download(filepath)

    def download_movie(self, movie_url):
        self._download_video(movie_url)

    def download_series(self, series_url, specific_episodes=None, nproc=1):
        episodes_urls = SeriesParser().get_episodes_urls(series_url)

        if specific_episodes:
            parsed_episodes = list(self._parse_episodes(specific_episodes))
            episodes_urls = [url for i, url in enumerate(episodes_urls, 1)
                             if i in parsed_episodes]

        if nproc > 1:
            with concurrent.futures.ProcessPoolExecutor(max_workers=nproc) as executor:
                executor.map(self._download_video, episodes_urls)
        else:
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
    def _get_file_name(name, ext='ts'):
        return f'{name}.{ext}'


def main():
    args = docopt.docopt(__doc__, argv=sys.argv[1:], version=__version__)
    segments = args.get('--segments') or DEFAULT_SIMULTANEOUS_SEGMENTS_COUNT
    ffmpeg_support = args.get('--ffmpeg')

    downloader = ATDownloader(directory=os.path.expanduser(args.get('<directory>') or os.getcwd()),
                              workers=int(segments), ffmpeg=ffmpeg_support)

    try:
        if args.get('movie'):
            downloader.download_movie(args.get('<movie_url>'))
        elif args.get('episode'):
            downloader.download_movie(args.get('<episode_url>'))
        elif args.get('series'):
            processes = args.get('--processes') or DEFAULT_PROCESSES_COUNT

            downloader.download_series(args.get('<series_url>'),
                                       args.get('--episodes'),
                                       nproc=int(processes))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
