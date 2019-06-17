from config import *
import datetime
import traceback
from datetime import time
import os

import gspread
from gspread_formatting import format_cell_range, Color, CellFormat, TextFormat
from oauth2client.service_account import ServiceAccountCredentials

import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, Filters, CallbackQueryHandler, MessageHandler
from telegram.ext.dispatcher import run_async

try:
    import convertapi
except ModuleNotFoundError:
    pass
import tempfile
from PIL import Image, ImageChops


def start(bot, update, job_queue):
    run_time = time(hour=RUN_HOUR, minute=RUN_MINUTE, second=RUN_SECONDS)
    job_queue.run_daily(how_was_your_day, time=run_time,
                        name='YearInPixel Daily Handler')
    update.message.reply_text('Hey!\nWelcome to Year in Pixels.')
    # job_queue.run_once(how_was_your_day, when=0)


def download(bot, update):
    def trim_space(im, border):
        bg = Image.new(im.mode, im.size, border)
        diff = ImageChops.difference(im, bg)
        bbox = diff.getbbox()
        if bbox:
            return im.crop(bbox)

    convertapi.api_secret = CONVERT_API_SECRET

    url = 'https://docs.google.com/spreadsheets/d/{}/export?format=xlsx&gid={}'.\
        format(GSPREADSHEET_ID, GSPREADSHEET_GID)
    fd, path = tempfile.mkstemp(suffix='.png')
    try:
        convertapi.convert('png', {
            'File': url
        }, from_format='xlsx').save_files(path)
        with Image.open(path) as image:
            image = trim_space(image, (255, 255, 255))
            image.save(path, quality=100)

        with open(path, 'rb') as doc:
            bot.send_photo(chat_id=update.message.chat_id,
                           photo=doc,
                           timeout=60)
    except Exception:
        traceback.print_exc()
        update.message.reply_text('_It was not possible to generate the image._',
                                  parse='Markdown')
    finally:
        try:
            os.close(fd)
            os.remove(path)
        except Exception:
            traceback.print_exc()
            pass


def answer_handler(bot, update):
    try:
        query = update.callback_query
        query_list = query.data.split('|')
        emotion = query_list[0]
        date = query_list[1]

        work_dir = os.path.dirname(os.path.realpath(__file__))
        google_api_local = os.path.normpath(
            '{}/google_api.json'.format(work_dir))

        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        credenciais = ServiceAccountCredentials.from_json_keyfile_name(
            google_api_local, scope)
        gsheet = gspread.authorize(credenciais)
        spreadsheet = gsheet.open_by_key(GSPREADSHEET_ID)
        worksheet = spreadsheet.worksheet(GSPREADSHEET_WORKSHEET)

        day = datetime.datetime.strptime(date, DATE_PATTERN).strftime('%d')
        month = datetime.datetime.strptime(date, DATE_PATTERN).strftime('%m')

        # Translate current month to it's appropriate column on the worksheet
        column = month \
            .replace('12', 'M') \
            .replace('11', 'L') \
            .replace('10', 'K') \
            .replace('09', 'J') \
            .replace('08', 'I') \
            .replace('07', 'H') \
            .replace('06', 'G') \
            .replace('05', 'F') \
            .replace('04', 'E') \
            .replace('03', 'D') \
            .replace('02', 'C') \
            .replace('01', 'B')

        # Translate current day to it's appropriate row on the worksheet
        # Row = Current day + 1
        row = str(int(day) + 1)

        clabel = '{}{}'.format(column, row)
        crange = '{}:{}'.format(clabel, clabel)

        if emotion == 'very_happy':
            color = Color(VERY_HAPPY_COLOR[0], VERY_HAPPY_COLOR[1],
                          VERY_HAPPY_COLOR[2])
            cell_format = CellFormat(backgroundColor=color,
                                     textFormat=TextFormat(
                                         foregroundColor=color),
                                     wrapStrategy='CLIP')
            worksheet.update_acell(clabel, 'Very Happy')
            format_cell_range(worksheet, crange, cell_format)

        elif emotion == 'happy':
            color = Color(HAPPY_COLOR[0], HAPPY_COLOR[1], HAPPY_COLOR[2])
            cell_format = CellFormat(backgroundColor=color,
                                     textFormat=TextFormat(
                                         foregroundColor=color),
                                     wrapStrategy='CLIP')
            worksheet.update_acell(clabel, 'Happy')
            format_cell_range(worksheet, crange, cell_format)

        elif emotion == 'neutral':
            color = Color(NEUTRAL_COLOR[0], NEUTRAL_COLOR[1], NEUTRAL_COLOR[2])
            cell_format = CellFormat(backgroundColor=color,
                                     textFormat=TextFormat(
                                         foregroundColor=color),
                                     wrapStrategy='CLIP')
            worksheet.update_acell(clabel, 'Neutral')
            format_cell_range(worksheet, crange, cell_format)

        elif emotion == 'sad':
            color = Color(SAD_COLOR[0], SAD_COLOR[1], SAD_COLOR[2])
            cell_format = CellFormat(backgroundColor=color,
                                     textFormat=TextFormat(
                                         foregroundColor=color),
                                     wrapStrategy='CLIP')
            worksheet.update_acell(clabel, 'Sad')
            format_cell_range(worksheet, crange, cell_format)

        elif emotion == 'very_sad':
            color = Color(VERY_SAD_COLOR[0], VERY_SAD_COLOR[1], VERY_SAD_COLOR[2])
            cell_format = CellFormat(backgroundColor=color,
                                     textFormat=TextFormat(
                                         foregroundColor=color),
                                     wrapStrategy='CLIP')
            worksheet.update_acell(clabel, 'Very Sad')
            format_cell_range(worksheet, crange, cell_format)

        responses = {'very_happy': '😄', 'happy': '🙂', 'neutral': '😐', 'sad': '🙁',
                     'very_sad': '😞'}
        current_response = responses[emotion]
        bot.edit_message_text(
            text='_{}: {}_'.format(date, current_response),
            chat_id=query.message.chat_id,
            message_id=query.message.message_id,
            parse_mode=telegram.ParseMode.MARKDOWN)
    except Exception:
        traceback.print_exc()


def how_was_your_day(bot, job):
    today_date = datetime.datetime.today().strftime(DATE_PATTERN)
    keyboard = [[InlineKeyboardButton('😄',
                                      callback_data='very_happy|{}'.format(
                                          today_date)),
                 InlineKeyboardButton('🙂',
                                      callback_data='happy|{}'.format(
                                          today_date)),
                 InlineKeyboardButton('😐',
                                      callback_data='neutral|{}'.format(
                                          today_date)),
                 InlineKeyboardButton('🙁',
                                      callback_data='sad|{}'.format(
                                          today_date)),
                 InlineKeyboardButton('😞',
                                      callback_data='very_sad|{}'.format(
                                          today_date))]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    msg = '*{}*\nHow was your day?'.format(today_date)
    bot.send_message(text=msg,
                     chat_id=TELEGRAM_USER_ID,
                     parse_mode='Markdown',
                     reply_markup=reply_markup)


@run_async
def unknow2(bot, update):
    update.message.reply_text('_I was not able to understand what you said._', parse_mode='Markdown')


@run_async
def unknow(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="_Sorry, not a valid command._",
                     parse_mode='Markdown')


def error(bot, update, erro):
    print('Update "{}" caused error "{}"'.format(update, erro))


def main():
    updater = Updater(BOT_TOKEN)

    updater.dispatcher.add_handler(
        CommandHandler('start', start, Filters.user(TELEGRAM_USER_ID),
                       pass_job_queue=True))
    if CONVERT_API_SECRET:
        updater.dispatcher.add_handler(
            CommandHandler('download', download, Filters.user(TELEGRAM_USER_ID)))
    updater.dispatcher.add_handler(CallbackQueryHandler(answer_handler))
    updater.dispatcher.add_handler(
        MessageHandler(Filters.command, unknow))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, unknow2))
    updater.dispatcher.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    main()
