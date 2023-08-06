"""
A Command-Line tool to download manga from MangaDex, written in Python
"""

__version__ = "1.0.2"
__description__ = "A Command-Line tool to download manga from MangaDex, written in Python"
__author__ = "mansuf"
__license__ = "MIT"
__repository__ = "https://github.com/mansuf/mangadex-downloader"

import logging
from .network import *
from .main import *
from .errors import *
from .manga import Manga, ContentRating
from .language import Language, get_language

logging.getLogger(__name__).addHandler(logging.NullHandler())