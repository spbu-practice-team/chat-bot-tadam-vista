from issue_manager import IssueManager

Gleb_token = "perm:cm9vdA==.NDYtMA==.yc2rmm8e2iecHUkPMBbKfXasd1fpx6"
Gleb_youtrack_domain = "testbotproject"
Gleb_issue_name = "DEMO-21"

GlebIssue = IssueManager(Gleb_youtrack_domain, Gleb_token)

print("\n  GET requests:")
x = GlebIssue.get_priority(Gleb_issue_name)
print(f"{x.name}: {x.value}")
x = GlebIssue.get_state(Gleb_issue_name)
print(f"{x.name}: {x.value}")
x = GlebIssue.get_time_start(Gleb_issue_name)
print(f"{x.name}: {x.value}")
x = GlebIssue.get_time_end(Gleb_issue_name)
print(f"{x.name}: {x.value}")

print("\n  POST requests:")
x = GlebIssue.update_priority(Gleb_issue_name, "Critical")
print(f"{x.name}: {x.value}")
x = GlebIssue.update_time_end(Gleb_issue_name, "5н 7д 3ч 2м")
print(f"{x.name}: {x.value}")
