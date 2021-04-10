
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler
)

from TG.ptb_handlers import (
    send_logs,
    call_handler
)

from TG.ptb_jobs import (
    get_uploads,
    vid_feed
)


def main():

    updater = Updater(
        token='BOT_TOKEN',
        use_context=True
                      )

    job = updater.job_queue

    job.run_repeating(callback=get_uploads, interval=86400, first=1)

    job.run_repeating(callback=vid_feed, interval=200, first=2)

    _dispatcher = updater.dispatcher

    _dispatcher.add_handler(CommandHandler('logs', send_logs))

    _dispatcher.add_handler(CallbackQueryHandler(callback=call_handler))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
