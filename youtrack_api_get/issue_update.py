import json
import httpx

priority_id = "111-0"
time_end_id = "117-0"


def update_priority(youtrack_domain, issue_name, token, priority):
    url = "https://" \
          + youtrack_domain \
          + ".myjetbrains.com/youtrack/api/issues/" \
          + issue_name \
          + "/customFields/" \
          + priority_id
    headers = {'Authorization': 'Bearer ' + token,
               "Content-Type": "application/json"
               }
    params = {'fields': 'projectCustomField(field(name)),value(name)'}
    data = {
        "projectCustomField": {
            "field": {
                "name": "Priority"
            }
        },
        "value": {
            "name": priority
        }
    }
    data = json.dumps(data)
    response = httpx.post(url, headers=headers, params=params, data=data)
    response_data = response.json()
    name = response_data["projectCustomField"]["field"]["name"]
    value = response_data["value"]["name"] if ("name" in response_data["value"]) else "has no"
    return name + ": " + value


def update_time_end(youtrack_domain, issue_name, token, time):
    url = "https://" \
          + youtrack_domain \
          + ".myjetbrains.com/youtrack/api/issues/" \
          + issue_name \
          + "/customFields/" \
          + time_end_id
    headers = {'Authorization': 'Bearer ' + token,
               "Content-Type": "application/json"
               }
    params = {'fields': 'projectCustomField(field(name)),value(presentation)'}
    data = {
        "projectCustomField": {
            "field": {
                "name": "Оценка"
            }
        },
        "value": {
            "presentation": time
        }
    }
    data = json.dumps(data)
    response = httpx.post(url, headers=headers, params=params, data=data)
    response_data = response.json()
    name = response_data["projectCustomField"]["field"]["name"]
    value = response_data["value"]["presentation"] if ("presentation" in response_data["value"]) else "has no"
    return name + ": " + value
