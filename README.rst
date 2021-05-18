arabic-toons-downloader
=======================

.. image:: https://api.codacy.com/project/badge/Grade/075b4dc6e5c74e42975c9a7b6226b16c
   :alt: Codacy Badge
   :target: https://www.codacy.com/app/mohan3d94/arabic-toons-downloader?utm_source=github.com&utm_medium=referral&utm_content=mohan3d/arabic-toons-downloader&utm_campaign=badger

arabic-toons-downloader is a program that can download movies and series
from `arabic-toons <http://www.arabic-toons.com>`_.

Installation
------------

.. code-block:: console

    Clone the project
    $ git clone https://github.com/mohan3d/arabic-toons-downloader.git

    Install dependencies
    $ cd arabic-toons-downloader
    $ pip install -r requirements.txt

Usage
-----

.. code-block:: console

    $ python downloader.py movie <movie_url> [<directory>] [options]
    $ python downloader.py episode <episode_url> [<directory>] [options]
    $ python downloader.py series <series_url> [<directory>] [options]

Examples
--------

.. code-block:: console

    Download Detective Conan movie 04
    $ python downloader.py movie http://www.arabic-toons.com/conan-film-23797-movies-streaming.html

    Download Detective Conan movie 04 (use segments option, might be faster depending on your connection speed)
    $ python downloader.py movie http://www.arabic-toons.com/conan-film-23797-movies-streaming.html -s 16
    $ python downloader.py movie http://www.arabic-toons.com/conan-film-23797-movies-streaming.html -s 32

    Download all Legend Tarzan episodes
    $ python downloader.py series http://www.arabic-toons.com/legend-tarzan-1405895019-anime-streaming.html

    Download all Legend Tarzan episodes
    (use segments option might be faster depending on your connection speed)
    (use processes option to download n episodes simultaneously)
    (in this case download 4 episodes at the same time)
    $ python downloader.py series http://www.arabic-toons.com/legend-tarzan-1405895019-anime-streaming.html -s 16 -p 4

    Download Detective Conan movie 04 - mp4 file using ffmpeg (ffmpeg must be installed and accessible for this script)
    (--ffmpeg can be used along with other options)
    $ python downloader.py movie http://www.arabic-toons.com/conan-film-23797-movies-streaming.html -s 16 --ffmpeg


Docker
------

.. code-block:: console

    Build docker image
    $ docker build -t "arabic-toons-downloader" .

    Create a new directory to save files locally
    $ mkdir ~/toons

    Run it
    $ docker run --rm -v ~/toons:/toons/ -it arabic-toons-downloader <SAME OPTIONS FROM USAGE>

    Example
    $ docker run --rm -v ~/toons:/toons/ -it arabic-toons-downloader series http://www.arabic-toons.com/conan-s1-1405901146-anime-streaming.html /toons/conans1
