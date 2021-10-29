from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from settings import AppSettings

config = AppSettings()


def main():
    bot = MatrixBotAPI(config.SERVER, config.USERNAME, config.PASSWORD)

    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()


if __name__ == "__main__":
    main()
