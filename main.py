from matrix_bot_api.matrix_bot_api import MatrixBotAPI
from matrix_bot_api.mcommand_handler import MCommandHandler
from resources import strings
from resources.regexp import datetime_exp
from settings import AppSettings
from youtrack_api.issue_manager import issue_manager
from resources.db import *

config = AppSettings()

BotStats.create_table()

def remove_first_argument(func):
    def the_wrapper(room, event):
        args = event['content']['body'].split()
        add_stats(room.client, args[0])
        args.pop(0)
        func(room, args)
    return the_wrapper


@remove_first_argument
def get_task_info(room, args):
    if not args:
        room.send_text(strings.INPUT_ISSUE_NAME_ERROR)
        return

    issue_name = args[0]
    state = issue_manager.get_state(issue_name)
    priority = issue_manager.get_priority(issue_name)
    start_time = issue_manager.get_time_start(issue_name)
    end_time = issue_manager.get_time_end(issue_name)

    task_info = strings.ISSUE_INFO_TEMPLATE.format(
        name=issue_name,
        state=state.value,
        priority=priority.value,
        start_time=start_time.value,
        end_time=end_time.value
    )

    room.send_text(task_info)

@remove_first_argument
def get_help(room, args):
    room.send_text(strings.INPUT_HELP)
    return

@remove_first_argument
def update_priority(room, args):
    if not args or len(args) == 1:
        room.send_text(strings.INPUT_PRIORITY_AND_ISSUE_NAME_ERROR)
        return

    issue_name = args[0]
    new_priority = args[1]
    if new_priority not in strings.POSSIBLE_PRIORITY:
        text = strings.INPUT_PRIORITY_ERROR
        room.send_text(text)
        return

    priority = issue_manager.update_priority(issue_name, new_priority)

    text = strings.SUCCESSFUL_UPDATE_PRIORITY.format(priority=priority.value, issue_name=issue_name)
    room.send_text(text)


@remove_first_argument
def update_time_end(room, args):

    if not args or len(args) == 1:
        room.send_text(strings.INPUT_END_DATETIME_AND_ISSUE_NAME_ERROR)
        return

    issue_name = args[0]
    new_end_time = ' '.join(args[1:])
    if not datetime_exp.match(new_end_time):
        text = strings.INPUT_END_DATETIME_ERROR
        room.send_text(text)
        return

    end_datetime = issue_manager.update_time_end(issue_name, new_end_time)

    text = strings.SUCCESSFUL_UPDATE_PRIORITY.format(priority=end_datetime.value, issue_name=issue_name)
    room.send_text(text)

@remove_first_argument
def post_comment(room, args):
    if not args or len(args) == 1:
        room.send_text(strings.INPUT_ISSUE_COMMENT_ERROR)
        return

    issue_name = args[0]
    new_comment = ' '.join(args[1:])
    
    comment = issue_manager.post_comment(issue_name, new_comment)
    if comment is None:
        text = strings.COMMENT_ADDED_WITH_ERROR
    else:
        text = strings.COMMENT_ADDED_SUCCESSFULLY

    room.send_text(text)
@remove_first_argument
def _get_stats(room, args):
    try:
        text = strings.STATS_USERS
        for stat in BotStats.select().group_by(BotStats.request, BotStats.client).order_by(BotStats.client, BotStats.count.desc()):
            text += strings.STATS_USER.format(stat.client, stat.request, str(stat.count))
        text += strings.STATS_REQUESTS
        for stat in BotStats.select(BotStats.request, fn.SUM(BotStats.count)).group_by(BotStats.request).order_by(BotStats.request):
            text += strings.STATS_REQUEST.format(stat.request, str(stat.count))
        room.send_text(text)
        return
    except:
        room.send_text(strings.STATS_CHANGE_ERROR)

def main():
    bot = MatrixBotAPI(config.SERVER, config.USERNAME, config.PASSWORD)

    get_task_info_handler = MCommandHandler("info", get_task_info)
    bot.add_handler(get_task_info_handler)

    update_priority_handler = MCommandHandler("priority", update_priority)
    bot.add_handler(update_priority_handler)

    update_end_datetime_handler = MCommandHandler("end_datetime", update_time_end)
    bot.add_handler(update_end_datetime_handler)

    get_help_handler = MCommandHandler("help", get_help)
    bot.add_handler(get_help_handler)

    post_comment_handler = MCommandHandler("comment", post_comment)
    bot.add_handler(post_comment_handler)

    _get_stats_handler = MCommandHandler("stats", _get_stats, '#')
    bot.add_handler(_get_stats_handler)

    #get_comment_text_handler = MCommandHandler("", get_comment_text)
    #bot.add_handler(get_comment_text_handler)

    bot.start_polling()

    # Infinitely read stdin to stall main thread while the bot runs in other threads
    while True:
        input()


if __name__ == "__main__":
    main()
