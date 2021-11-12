import httpx
import datetime
import json
from settings import AppSettings
from youtrack_api.schemas.field_info import FieldInfo

config = AppSettings()


class IssueManager:
    state_id = "111-2"
    priority_id = "111-0"
    time_end_id = "117-0"
    comment_id = "4-2"

    def __init__(self, youtrack_domain, token):
        self.youtrack_domain = youtrack_domain
        self.token = token
        self.base_url = f"https://{youtrack_domain}.myjetbrains.com/youtrack/api/issues"

    def _get_custom_field(self, issue_name, field_id):
        url = f"{self.base_url}/{issue_name}/customFields/{field_id}"
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

    def get_state(self, issue_name):
        return self._get_custom_field(issue_name, IssueManager.state_id)

    def get_priority(self, issue_name):
        return self._get_custom_field(issue_name, IssueManager.priority_id)

    def get_time_end(self, issue_name):
        url = f"{self.base_url}/{issue_name}/customFields/{IssueManager.time_end_id}"
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

    


    def get_time_start(self, issue_name):
        url = f"{self.base_url}/{issue_name}"
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

    def update_priority(self, issue_name, priority):
        url = f"{self.base_url}/{issue_name}/customFields/{IssueManager.priority_id}"
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

    def update_time_end(self, issue_name, time):
        url = f"{self.base_url}/{issue_name}/customFields/{IssueManager.time_end_id}"
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

 
    def post_comment(self, issue_name, comment):
        url = f"{self.base_url}/{issue_name}/comments/{IssueManager.comment_id}"
        headers = {'Authorization': f"Bearer {self.token}",
                   "Content-Type": "application/json"}
        params = {'fields': 'comment(text)'}
        data = {
            "comment":{
                "text": comment
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
        name = response_data["comment"]["name"]
        value = response_data["comment"]["text"] if ((response_data["comment"] is not None) and ("text" in response_data["comment"])) else None
        return FieldInfo(name=name, value=value)

    def get_comment(self, issue_name):
        url = f"{self.base_url}/{issue_name}/comments/{IssueManager.comment_id}"
        headers = {'Authorization': f"Bearer {self.token}"}
        params = {'fields': 'comments(field(name)),value(name)'}
        response = httpx.get(url, headers=headers, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPError as e:
            print(e)
            return None
        response_data = response.json()
        name = response_data["projectCustomField"]["field"]["name"]
        value = response_data["comment"]["text"] if ((response_data["comment"] is not None) and ("text" in response_data["comment"])) else None
        return FieldInfo(name=name, value=value)

        
        

    


issue_manager = IssueManager(config.DOMAIN, config.TOKEN)
