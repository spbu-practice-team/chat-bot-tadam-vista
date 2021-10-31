import httpx
import datetime

state_id = "111-2"
priority_id = "111-0"
time_end_id = "117-0"


def get_custom_field(youtrack_domain, issue_name, field_id, token):
    url = "https://" \
          + youtrack_domain \
          + ".myjetbrains.com/youtrack/api/issues/" \
          + issue_name \
          + "/customFields/" \
          + field_id
    headers = {'Authorization': 'Bearer ' + token}
    params = {'fields': 'projectCustomField(field(name)),value(name)'}
    response = httpx.get(url, headers=headers, params=params)
    data = response.json()
    name = data["projectCustomField"]["field"]["name"]
    value = data["value"]["name"] if ("name" in data["value"]) else "has no"
    return name + ": " + value


def get_state(youtrack_domain, issue_name, token):
    return get_custom_field(youtrack_domain, issue_name, state_id, token)


def get_priority(youtrack_domain, issue_name, token):
    return get_custom_field(youtrack_domain, issue_name, priority_id, token)


def get_time_end(youtrack_domain, issue_name, token):
    return get_custom_field(youtrack_domain, issue_name, time_end_id, token)


def get_time_start(youtrack_domain, issue_name, token):
    url = "https://" \
               + youtrack_domain \
               + ".myjetbrains.com/youtrack/api/issues/"\
               + issue_name
    headers = {'Authorization': 'Bearer ' + token}
    params = {'fields': 'created'}
    response = httpx.get(url, headers=headers, params=params)
    data = response.json()
    name = "Created: "
    time = data["created"]
    value = datetime.datetime.fromtimestamp(time//1000.0)
    return name + ": " + str(value)
