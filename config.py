import os
from typing import Final
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BOT_TOKEN: Final[str] = os.getenv('BOT_TOKEN', 'define me')
OWNER_IDS: Final[tuple] = tuple(int(i) for i in str(os.getenv('BOT_OWNER_IDS')).split(','))

# Информация о канале, в который постить заявки
PUBLICATION_CHANNEL_ID = -1001267498399
APPROVING_CHANNEL_ID = -1002023658145
