# YearInPixelsBot
Generate a pretty overview from your year right on your telegram.


This is a Telegram Bot.

It currently only supports a single user using it.

Don't forget to generate your google_api.json and put it on root. Refer to [this tutorial on how to do it for gspread.](https://gspread.readthedocs.io/en/latest/oauth2.html)

Edit config.py to add your own variables.

Install the librarys on requirements.txt.

It is designed to work on [this model spreadsheet](https://docs.google.com/spreadsheets/d/1_4w_bPqcOlyncrgL29edU5Vwcibc67GyMEYabb7N6So/edit?usp=sharing), copy it and configure according on config.py. Any changes to the overall position of rows and columns will need to be reflected on the code, but all the rest is fair game.