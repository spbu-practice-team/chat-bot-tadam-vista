"""Api exceptions."""


class APIError(Exception):
    pass


class InvalidIssueParams(APIError):
    pass
