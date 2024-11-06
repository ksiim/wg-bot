from dotenv import load_dotenv
import os

load_dotenv()  # Загрузка переменных из .env файла

BOT_TOKEN = os.getenv('BOT_TOKEN')
PUBLIC_KEY = os.getenv('PUBLIC_KEY')
PRIVATE_KEY = os.getenv('PRIVATE_KEY')