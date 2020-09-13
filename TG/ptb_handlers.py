from telegram import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

from .ptb_funcs import del_mes


def send_logs(update, context):
    if update.effective_user.id == 399835396:
        keyboard = [[InlineKeyboardButton(text='❌ Delete', callback_data='del')]]
        context.bot.send_document(
            chat_id=update.effective_user.id,
            document=open('./logs.txt', 'rb'),
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        del_mes(_update=update, _context=context)


def call_handler(update, context):
    call = update.callback_query

    if call.data == 'del':
        del_mes(_update=call, _context=context)


