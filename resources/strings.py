from typing import Any, Protocol, cast

from mako.lookup import TemplateLookup


class FormatTemplate(Protocol):
    """
    Protocol for correct templates typing.

    Allow use format() instead of render() method that needed to maintain consistency
    with regular string formatting.
    """

    def format(self, **kwargs: Any) -> str:  # noqa: WPS125 A003
        """Render template."""


class TemplateFormatterLookup(TemplateLookup):
    """Represent a collection of templates from the local filesystem."""

    def get_template(self, uri: str) -> FormatTemplate:
        """Cast default mako template to FormatTemplate."""

        def _format(**kwargs: Any) -> str:  # noqa: WPS430
            return template.render(**kwargs).rstrip()

        template = super().get_template(uri)
        template.format = _format  # noqa: WPS125
        return cast(FormatTemplate, template)


lookup = TemplateFormatterLookup(
    directories=["resources/templates"],
    input_encoding="utf-8",
    strict_undefined=True,
)
OUTPUT_DATE_FORMAT = "DD MMMM YYYY"
INPUT_DATETIME_FORMAT = "1н 1д 1ч 1м"
ISSUE_INFO_TEMPLATE = lookup.get_template("task_info.txt.mako")
POSSIBLE_PRIORITY = ("Show-stopper", "Critical", "Major", "Normal", "Minor")
INPUT_ISSUE_NAME_ERROR = "Введите вместе с командой номер заявки или ключевые слова!"
INPUT_PRIORITY_AND_ISSUE_NAME_ERROR = f"Введите вместе с командой номер заявки или ключевые слова и новое значение приоритета из предложенных:\n{', '.join(POSSIBLE_PRIORITY)}"
INPUT_END_DATETIME_AND_ISSUE_NAME_ERROR = f"Введите вместе с командой номер заявки или ключевые слова и новое значение оценочного времени выполнения задачи:"
SUCCESSFUL_UPDATE_PRIORITY = "Приоритет {priority} для задачи {issue_name} установлен"
INPUT_PRIORITY_ERROR = f"Введите приоритет из предложенных ниже:\n{', '.join(POSSIBLE_PRIORITY)}"
INPUT_END_DATETIME_ERROR = f"Введите оценочное время выполнения задачи как написано ниже:\n{INPUT_DATETIME_FORMAT}"
INPUT_HELP = "Список доступных команд: \n \t - !priority – изменить приоритет \n \t - !time – изменить время выполнения задачи \n \t - !comment – добавить комментарий к задаче \n \t - !info – вся информация о задаче \n"
COMMENT_ADDED_SUCCESSFULLY = "Комментарий успешно добавлен \n"
COMMENT_ADDED_WITH_ERROR = "Ошибка при добавлении комментария \n"
INPUT_ISSUE_COMMENT_ERROR = "Введите вместе с командой номер заявки и комментарий \n"
STATS_CHANGE_ERROR = "Ошибка при попытке вывести статистику\n"
STATS_USER = "Пользователь \"{}\" вызывал команду \"{}\" {} раз(а)\n"
STATS_USERS = "Статистика по пользователям:\n"
STATS_REQUESTS = "Статистика по командам:\n"
STATS_REQUEST = "Команда \"{}\" была вызвана {} раз(а)\n"
