import unittest

import downloader


class TestVideoParser(unittest.TestCase):
    def setUp(self) -> None:
        self.video_parser = downloader.VideoParser()

    def tearDown(self) -> None:
        self.video_parser.close()

    def test_get_stream_url(self):
        video_parser = self.video_parser
        video_parser.get_stream_url = video_parser.get_stream_info

        cases = [
            ('http://www.arabic-toons.com/legend-tarzan-1405895019-24796.html', 'legend_tarzan_05.mp4/playlist.m3u8',
             'اسطورة طرزان الحلقة 5'),
            (
            'http://www.arabic-toons.com/al7deqa-alseria-1405898769-24316.html', 'al7deqa_alseria_18.mp4/playlist.m3u8',
            'الحديقة السرية الحلقة 18'),
            ('http://www.arabic-toons.com/dai-1405896719-24551.html', 'dai_39.mp4/playlist.m3u8',
             'داي الشجاع الحلقة 39'),
            (
            'http://www.arabic-toons.com/papay-1405900079-24109.html', 'papay_11.mp4/playlist.m3u8', 'باباي الحلقة 11'),
            ('http://www.arabic-toons.com/beyblade-s2-1467019937-24996.html', 'beyblade_s2_23.mp4/playlist.m3u8',
             'بي بليد الموسم 2 الحلقة 23'),
        ]

        for url, expected_url_suffix, expected_title in cases:
            actual_url, actual_title = self.video_parser.get_stream_info(url)

            self.assertTrue((expected_url_suffix in actual_url))
            self.assertEqual(expected_title, actual_title)


class TestSeriesParser(unittest.TestCase):
    def setUp(self) -> None:
        self.series_parser = downloader.SeriesParser()

    def tearDown(self) -> None:
        self.series_parser.close()

    def test_get_episodes_urls(self):
        cases = [
            ("http://www.arabic-toons.com/legend-tarzan-1405895019-anime-streaming.html", 35),
            ("http://www.arabic-toons.com/calimero-s1-1405894466-anime-streaming.html", 56),
            ("http://www.arabic-toons.com/madrast-kungfu-1405900472-anime-streaming.html", 20),
            ("http://www.arabic-toons.com/al8na9-1407653461-anime-streaming.html", 70),
            ("http://www.arabic-toons.com/sabeq-wa-la7eq-s1-1415604494-anime-streaming.html", 51),
        ]

        for url, expected_episodes_count in cases:
            actual_episodes = self.series_parser.get_episodes_urls(url)

            self.assertEqual(len(actual_episodes), expected_episodes_count)


if __name__ == '__main__':
    unittest.main()
