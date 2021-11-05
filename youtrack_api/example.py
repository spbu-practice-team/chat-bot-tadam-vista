from IssueManager import IssueManager

Gleb_token = "perm:cm9vdA==.NDYtMA==.yc2rmm8e2iecHUkPMBbKfXasd1fpx6"
Gleb_youtrack_domain = "testbotproject"
Gleb_issue_name = "DEMO-21"

GlebIssue = IssueManager(Gleb_issue_name, Gleb_youtrack_domain, Gleb_token)

print("\n  GET requests:")
x = GlebIssue.get_priority()
print(f"{x.name}: {x.value}")
x = GlebIssue.get_state()
print(f"{x.name}: {x.value}")
x = GlebIssue.get_time_start()
print(f"{x.name}: {x.value}")
x = GlebIssue.get_time_end()
print(f"{x.name}: {x.value}")

print("\n  POST requests:")
x = GlebIssue.update_priority("Critical")
print(f"{x.name}: {x.value}")
x = GlebIssue.update_time_end("5н 7д 3ч 2м")
print(f"{x.name}: {x.value}")
