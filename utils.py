from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

REPO = 'https://github.com/nuhmanpk/WebScrapper/'

FINISHED_PROGRESS_STR = "▓"
UN_FINISHED_PROGRESS_STR = "░"

START_TEXT = "Hello , I am a web scrapper bot.\nSend me any link for scrapping.\n\nJoin @BugHunterBots"

START_BUTTON = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('Raw Data', callback_data='cbrdata'),
            InlineKeyboardButton('HTML Data', callback_data='cbhtmldata')
        ],
        [
            InlineKeyboardButton('All Links', callback_data='cballlinks'),
            InlineKeyboardButton(
                'All Paragraphs', callback_data='cballparagraphs')
        ],
        [
            InlineKeyboardButton('All Images', callback_data='cballimages')
        ]
    ]
)

CLOSE_BUTTON = InlineKeyboardMarkup(
    [[InlineKeyboardButton('Back', callback_data='cbclose')]]
)

OPTIONS = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton('Raw Data', callback_data='cbrdata',),
                InlineKeyboardButton('HTML Data', callback_data='cbhtmldata')
            ],
            [
                InlineKeyboardButton('All Links', callback_data='cballlinks'),
                InlineKeyboardButton(
                    'All Paragraphs', callback_data='cballparagraphs')
            ],
            [
                InlineKeyboardButton('All Images', callback_data='cballimages')
            ],
            [
                InlineKeyboardButton('All Audio', callback_data='cballaudio',),
                InlineKeyboardButton('All Video', callback_data='cballvideo')
            ]
        ]
    )