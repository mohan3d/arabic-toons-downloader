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


if __name__ == '__main__':
    unittest.main()
