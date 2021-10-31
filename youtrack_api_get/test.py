from issue_info import *

Gleb_token = "perm:cm9vdA==.NDYtMA==.yc2rmm8e2iecHUkPMBbKfXasd1fpx6"
Gleb_youtrack_domain = "testbotproject"
Gleb_issue_name = "DEMO-20"

status = get_state(Gleb_youtrack_domain, Gleb_issue_name, Gleb_token)
print(status)
priority = get_priority(Gleb_youtrack_domain, Gleb_issue_name, Gleb_token)
print(priority)
timeEnd = get_time_end(Gleb_youtrack_domain, Gleb_issue_name, Gleb_token)
print(timeEnd)
timeStart = get_time_start(Gleb_youtrack_domain, Gleb_issue_name, Gleb_token)
print(timeStart)
