import httpx
import datetime
import json
from schemas.FieldInfo import FieldInfo


class IssueManager:
    state_id = "111-2"
    priority_id = "111-0"
    time_end_id = "117-0"

    def __init__(self, issue_name, youtrack_domain, token):
        self.issue_name = issue_name
        self.youtrack_domain = youtrack_domain
        self.token = token
        self.base_url = f"https://{youtrack_domain}.myjetbrains.com/youtrack/api/issues/{issue_name}"

    def _get_custom_field(self, field_id):
        url = f"{self.base_url}/customFields/{field_id}"
        headers = {'Authorization': f"Bearer {self.token}"}
        params = {'fields': 'projectCustomField(field(name)),value(name)'}
        response = httpx.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            return None
        response_data = response.json()
        name = response_data["projectCustomField"]["field"]["name"]
        value = response_data["value"]["name"] if ((response_data["value"] is not None) and ("name" in response_data["value"])) else None
        return FieldInfo(name=name, value=value)

    def get_state(self):
        return self._get_custom_field(IssueManager.state_id)

    def get_priority(self):
        return self._get_custom_field(IssueManager.priority_id)

    def get_time_end(self):
        url = f"{self.base_url}/customFields/{IssueManager.time_end_id}"
        headers = {'Authorization': f"Bearer {self.token}"}
        params = {'fields': 'projectCustomField(field(name)),value(presentation)'}
        response = httpx.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            return None
        response_data = response.json()
        name = response_data["projectCustomField"]["field"]["name"]
        value = response_data["value"]["presentation"] if ((response_data["value"] is not None) and ("presentation" in response_data["value"])) else None
        return FieldInfo(name=name, value=value)

    def get_time_start(self):
        url = self.base_url
        headers = {'Authorization': f"Bearer {self.token}"}
        params = {'fields': 'created'}
        response = httpx.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            return None
        response_data = response.json()
        name = "Created: "
        time = response_data["created"]
        value = datetime.datetime.fromtimestamp(time // 1000.0)
        return FieldInfo(name=name, value=value)

    def update_priority(self, priority):
        url = f"{self.base_url}/customFields/{IssueManager.priority_id}"
        headers = {'Authorization': f"Bearer {self.token}",
                   "Content-Type": "application/json"}
        params = {'fields': 'projectCustomField(field(name)),value(name)'}
        data = {
            "projectCustomField": {
                "field": {
                    "name": "Priority"
                }
            },
            "value": {
                "name": priority  # Возможные значения приоритета: Show-stopper, Critical, Major, Normal, Minor
            }
        }
        data = json.dumps(data, indent=4)
        response = httpx.post(url, headers=headers, params=params, data=data)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            return None
        response_data = response.json()
        name = response_data["projectCustomField"]["field"]["name"]
        value = response_data["value"]["name"] if ((response_data["value"] is not None) and ("name" in response_data["value"])) else None
        return FieldInfo(name=name, value=value)

    def update_time_end(self, time):
        url = f"{self.base_url}/customFields/{IssueManager.time_end_id}"
        headers = {'Authorization': f"Bearer {self.token}",
                   "Content-Type": "application/json"}
        params = {'fields': 'projectCustomField(field(name)),value(presentation)'}
        data = {
            "projectCustomField": {
                "field": {
                    "name": "Оценка"
                }
            },
            "value": {
                "presentation": time  # Оценочное время в формате 1н 1д 1ч 1м
            }
        }
        data = json.dumps(data, indent=4)
        response = httpx.post(url, headers=headers, params=params, data=data)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            return None
        response_data = response.json()
        name = response_data["projectCustomField"]["field"]["name"]
        value = response_data["value"]["presentation"] if ((response_data["value"] is not None) and ("presentation" in response_data["value"])) else None
        return FieldInfo(name=name, value=value)
