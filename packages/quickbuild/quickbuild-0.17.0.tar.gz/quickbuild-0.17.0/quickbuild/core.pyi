from _typeshed import Incomplete
from quickbuild.endpoints import Agents as Agents, Audits as Audits, Authorizations as Authorizations, Builds as Builds, Changes as Changes, Configurations as Configurations, Dashboards as Dashboards, Groups as Groups, Identifiers as Identifiers, Issues as Issues, Measurements as Measurements, Memberships as Memberships, Nodes as Nodes, Profiles as Profiles, Reports as Reports, Requests as Requests, Resources as Resources, Shares as Shares, System as System, Tokens as Tokens, Users as Users
from quickbuild.exceptions import QBError as QBError, QBForbiddenError as QBForbiddenError, QBNotFoundError as QBNotFoundError, QBProcessingError as QBProcessingError, QBServerError as QBServerError
from quickbuild.helpers import ContentType as ContentType
from typing import NamedTuple, Optional

CONTENT_JSON: str

class Response(NamedTuple):
    status: Incomplete
    headers: Incomplete
    body: Incomplete

class QuickBuild:
    agents: Incomplete
    audits: Incomplete
    authorizations: Incomplete
    builds: Incomplete
    changes: Incomplete
    configurations: Incomplete
    dashboards: Incomplete
    groups: Incomplete
    identifiers: Incomplete
    issues: Incomplete
    measurements: Incomplete
    memberships: Incomplete
    nodes: Incomplete
    profiles: Incomplete
    reports: Incomplete
    requests: Incomplete
    resources: Incomplete
    shares: Incomplete
    system: Incomplete
    tokens: Incomplete
    users: Incomplete
    def __init__(self, content_type: Optional[ContentType]) -> None: ...
