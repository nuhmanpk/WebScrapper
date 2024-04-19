# /usr/bin/nuhmanpk/bughunter0 

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

BACK_BUTTON = [[InlineKeyboardButton('Back', callback_data='cbclose')]]

CLOSE_BUTTON = InlineKeyboardMarkup(
    BACK_BUTTON
)

OPTIONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('📄 Full Content', callback_data='cbrdata'),
            InlineKeyboardButton('📝 HTML Data', callback_data='cbhtmldata')
        ],
        [
            InlineKeyboardButton('🔗 All Links', callback_data='cballlinks'),
            InlineKeyboardButton('📃 All Paragraphs'
                                , callback_data='cballparagraphs')
        ],
        [
            InlineKeyboardButton('🌄 All Images', callback_data='cballimages')
        ],
        [
            InlineKeyboardButton('🎵 All Audio', callback_data='cballaudio'),
            InlineKeyboardButton('🎥 All Video', callback_data='cballvideo')
        ],
        [
            InlineKeyboardButton('📚 All PDFs', callback_data='cballpdf')
        ],
        [
            InlineKeyboardButton('🍪 Cookies', callback_data='cbcookies'),
            InlineKeyboardButton(
                '📦 LocalStorage', callback_data='cblocalstorage')
        ],
        [
            InlineKeyboardButton('📊 Metadata', callback_data='cbmetadata')
        ],
        # [
        #     InlineKeyboardButton('📷 Screenshot', callback_data='cbscreenshot'),
        #     InlineKeyboardButton('🎬 Screen Record', callback_data='cbscreenrecord')
        # ],
        [
            InlineKeyboardButton('🕷️ Crawl Complete Web', callback_data='cbcrawl')
        ],
    ]
)
