import os
import pathlib

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
HOME = str(pathlib.Path.home())
DATABASE_PATH = os.path.join(HOME, 'bot_database')
