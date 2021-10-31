from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mcommand_handler import MCommandHandler
from resources import strings
from settings import AppSettings

# Import your_api_adapter
# from services.api import your_api_adapter

config = AppSettings()


def remove_first_argument(func):
    def the_wrapper(room, event):
        args = event['content']['body'].split()
        args.pop(0)
        func(room, args)
    return the_wrapper


@remove_first_argument
def get_task_info(room, args):
    if not args:
        room.send_text(strings.INPUT_TASK_ID_OR_NAME_ERROR)
        return

    task_id = args[0]
    your_api_adapter.get_task_info(task_id)

    room.send_text("Done")


def main():
    bot = MatrixBotAPI(config.SERVER, config.USERNAME, config.PASSWORD)

    get_task_info_handler = MCommandHandler("info", get_task_info)
    bot.add_handler(get_task_info_handler)

    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()


if __name__ == "__main__":
    main()
