from IssueManager import IssueManager

Gleb_token = "perm:cm9vdA==.NDYtMA==.yc2rmm8e2iecHUkPMBbKfXasd1fpx6"
Gleb_youtrack_domain = "testbotproject"
Gleb_issue_name = "DEMO-21"

GlebIssue = IssueManager(Gleb_issue_name, Gleb_youtrack_domain, Gleb_token)

print("\n  GET requests:")
GlebIssue.get_priority().show()
GlebIssue.get_state().show()
GlebIssue.get_time_start().show()
GlebIssue.get_time_end().show()

print("\n  POST requests:")
GlebIssue.update_priority("Major").show()
GlebIssue.update_time_end("4н 2д 1ч 7м").show()
