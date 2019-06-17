BOT_TOKEN = ''  # [str] The telegram bot token
TELEGRAM_USER_ID = 22213123213  # [int]| List[int] | Will only answer messages from this user

RUN_HOUR = 23  # [int] Hour to be asked how your day was, in 24hour format
RUN_MINUTE = 59  # [int] Minute to be asked how your day was, in 24hour format
RUN_SECONDS = 0  # [int] Second to be asked how your day was, in 24hour format

DATE_PATTERN = '%d/%m/%Y'  # [str] Use python's datetime strftime patterns

GSPREADSHEET_ID = ''
GSPREADSHEET_WORKSHEET = ''
GSPREADSHEET_GID = '0'

VERY_HAPPY_COLOR = [1, 0.4117647, 0.38039216]           # rgb: ff6961
HAPPY_COLOR = [1, 0.7019608, 0.2784314]                 # rgb: ffb347
NEUTRAL_COLOR = [0.99215686, 0.99215686, 0.5882353]     # rgb: fdfd96
SAD_COLOR = [0.46666667, 0.8666667, 0.46666667]         # rgb: 48d148
VERY_SAD_COLOR = [0.46666667, 0.61960787, 0.79607844]   # rgb: 779ecb

CONVERT_API_SECRET = ''  # [str]  https://www.convertapi.com/ | Set to False if you want to disable it
