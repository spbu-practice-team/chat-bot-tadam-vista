<%
from resources.strings import OUTPUT_DATE_FORMAT
import pendulum
%>
Информация по заданию ${name}:
Статус: ${state}
Приоритет: ${priority}
Время создания задачи: ${pendulum.instance(start_time).format(OUTPUT_DATE_FORMAT, locale='ru')}
Время окончания: ${pendulum.instance(end_time).format(OUTPUT_DATE_FORMAT, locale='ru') if end_time else "—"}
