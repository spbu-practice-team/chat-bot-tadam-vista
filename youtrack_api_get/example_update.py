from issue_update import *

Gleb_token = "perm:cm9vdA==.NDYtMA==.yc2rmm8e2iecHUkPMBbKfXasd1fpx6"
Gleb_youtrack_domain = "testbotproject"
Gleb_issue_name = "DEMO-21"

# Возможные значения приоритета: Show-stopper, Critical, Major, Normal, Minor
priority = "Critical"

# Оценочное время в формате 1н 1д 1ч 1м
time = "3н 2д 6ч 13м"

answer1 = update_priority(Gleb_youtrack_domain, Gleb_issue_name, Gleb_token, priority)
print(answer1)
answer2 = update_time_end(Gleb_youtrack_domain, Gleb_issue_name, Gleb_token, time)
print(answer2)
