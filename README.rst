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

    $ python downloader.py movie <movie_url> [<directory>]
    $ python downloader.py episode <episode_url> [<directory>]
    $ python downloader.py series <series_url> [<directory>] [options]

Examples
--------

.. code-block:: console

    Download all Legend Tarzan episodes
    $ python downloader.py series http://www.arabic-toons.com/legend-tarzan-1405895019-anime-streaming.html

    Download Detective Conan movie 04
    $ python downloader.py movie http://www.arabic-toons.com/conan-film-23797-movies-streaming.html
