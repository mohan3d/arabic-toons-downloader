import downloader
import unittest


class TestVideoParser(unittest.TestCase):
    def test_get_stream_url(self):
        video_parser = downloader.VideoParser()

        self.assertEqual("rtmp://176.9.40.23/anime/legend_tarzan_05.mp4?code=",
                         video_parser.get_stream_url(
                             "http://www.arabic-toons.com/legend-tarzan-1405895019-24796.html#sets"))

        self.assertEqual("rtmp://176.9.40.23/anime/al7deqa_alseria_18.mp4?code=",
                         video_parser.get_stream_url(
                             "http://www.arabic-toons.com/al7deqa-alseria-1405898769-24316.html#sets"))

        self.assertEqual("rtmp://176.9.40.23/anime/dai_39.mp4?code=",
                         video_parser.get_stream_url(
                             "http://www.arabic-toons.com/dai-1405896719-24551.html#sets"))

        self.assertEqual("rtmp://176.9.40.23/anime/papay_11.mp4?code=",
                         video_parser.get_stream_url(
                             "http://www.arabic-toons.com/papay-1405900079-24109.html#sets"))

        self.assertEqual("rtmp://176.9.40.23/anime/beyblade_s2_23.mp4?code=",
                         video_parser.get_stream_url(
                             "http://www.arabic-toons.com/beyblade-s2-1467019937-24996.html#sets"))


class TestSeriesParser(unittest.TestCase):
    def test_get_episodes_urls(self):
        series_parser = downloader.SeriesParser()

        self.assertEqual(35, len(series_parser.get_episodes_urls(
            "http://www.arabic-toons.com/legend-tarzan-1405895019-anime-streaming.html")))

        self.assertEqual(56, len(series_parser.get_episodes_urls(
            "http://www.arabic-toons.com/calimero-s1-1405894466-anime-streaming.html")))

        self.assertEqual(20, len(series_parser.get_episodes_urls(
            "http://www.arabic-toons.com/madrast-kungfu-1405900472-anime-streaming.html")))

        self.assertEqual(70, len(series_parser.get_episodes_urls(
            "http://www.arabic-toons.com/al8na9-1407653461-anime-streaming.html")))

        self.assertEqual(51, len(series_parser.get_episodes_urls(
            "http://www.arabic-toons.com/sabeq-wa-la7eq-s1-1415604494-anime-streaming.html")))


if __name__ == '__main__':
    unittest.main()
