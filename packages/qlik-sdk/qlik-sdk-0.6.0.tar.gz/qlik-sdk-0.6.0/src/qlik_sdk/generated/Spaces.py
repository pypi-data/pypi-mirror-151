# This is spectacularly generated code by spectacular v0.0.0 based on
# Qlik Cloud Services Grafana 1.0.0-202205031030

from __future__ import annotations
from typing import Iterator, Union
from dataclasses import dataclass, asdict, is_dataclass
import io
import itertools
import warnings
from ..auth import Auth, Config
from ..listable import ListableResource
from ..rpc import RpcSession


@dataclass
class Space:
    """
    A space is a security context simplifying the management of access control by allowing users to control it on the containers instead of on the resources themselves.

    Attributes
    ----------
    id: str
    links: object
    name: str
      The name of the space. Personal spaces do not have a name.
    tenantId: str
    createdAt: str
    createdBy: str
      The ID of the user who created the space.
    description: str
      The description of the space. Personal spaces do not have a description.
    meta: object
    ownerId: str
      The user ID of the space owner.
    type: str
    updatedAt: str
    """

    id: str = None
    links: object = None
    name: str = None
    tenantId: str = None
    createdAt: str = None
    createdBy: str = None
    description: str = None
    meta: object = None
    ownerId: str = None
    type: str = None
    updatedAt: str = None

    def __init__(self_, **kvargs):
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ is self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ is self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]

    def get_raw_space(self) -> RawSpace:
        """
        Deprecated
        Retrieves a raw space by ID that the current user has access to.
        Retrieve a single raw space by ID.

        This endpoint only returns the space if the current user has an assignment in the space.

        It returns the minimum amount of information to characterize the assignments of the current user in this space.

        Supports all space types: shared and managed.

        Parameters
        ----------
        """
        warnings.warn("get_raw-space is deprecated", DeprecationWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/raw-spaces/{spaceId}".replace("{spaceId}", self.id),
            method="GET",
            params={},
            data=None,
        )
        obj = RawSpace(**response.json())
        obj.auth = self.auth
        return obj

    def delete(self) -> None:
        """
        Deprecated
        Deletes a space.

        Parameters
        ----------
        """
        warnings.warn("delete is deprecated", DeprecationWarning, stacklevel=2)

        self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="DELETE",
            params={},
            data=None,
        )

    def patch(self, body: SpacePatch) -> Space:
        """
        Deprecated
        Experimental
        Patches (updates) a space (partially).

        Parameters
        ----------
        body: SpacePatch
        """
        warnings.warn("patch is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("patch is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PATCH",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def set(self, body: SpaceUpdate) -> Space:
        """
        Deprecated
        Experimental
        Updates a space.

        Parameters
        ----------
        body: SpaceUpdate
        """
        warnings.warn("set is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("set is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", self.id),
            method="PUT",
            params={},
            data=data,
        )
        self.__init__(**response.json())
        return self

    def get_assignments(
        self, limit: int = None, next: str = None, prev: str = None, max_items=10
    ) -> ListableResource[Assignment]:
        """
        Deprecated
        Retrieves the assignments of the space matching the query.

        Parameters
        ----------
        limit: int = None
        next: str = None
        prev: str = None
        """
        warnings.warn("get_assignments is deprecated", DeprecationWarning, stacklevel=2)
        query_params = {}
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Assignment,
            auth=self.auth,
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            max_items=max_items,
            query_params=query_params,
        )

    def create_assignment(self, body: AssignmentCreate) -> Assignment:
        """
        Deprecated
        Creates an assignment.

        Parameters
        ----------
        body: AssignmentCreate
        """
        warnings.warn(
            "create_assignment is deprecated", DeprecationWarning, stacklevel=2
        )

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments".replace("{spaceId}", self.id),
            method="POST",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj


@dataclass
class Assignment:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    id: str
    links: object
    roles: list[str]
      The roles assigned to a user or group. Must not be empty.
    spaceId: str
    tenantId: str
    type: str
    createdAt: str
    createdBy: str
      The ID of the user who created the assignment.
    updatedAt: str
    """

    assigneeId: str = None
    id: str = None
    links: object = None
    roles: list[str] = None
    spaceId: str = None
    tenantId: str = None
    type: str = None
    createdAt: str = None
    createdBy: str = None
    updatedAt: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                is self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "spaceId" in kvargs:
            if type(kvargs["spaceId"]).__name__ is self_.__annotations__["spaceId"]:
                self_.spaceId = kvargs["spaceId"]
            else:
                self_.spaceId = kvargs["spaceId"]
        if "tenantId" in kvargs:
            if type(kvargs["tenantId"]).__name__ is self_.__annotations__["tenantId"]:
                self_.tenantId = kvargs["tenantId"]
            else:
                self_.tenantId = kvargs["tenantId"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "createdAt" in kvargs:
            if type(kvargs["createdAt"]).__name__ is self_.__annotations__["createdAt"]:
                self_.createdAt = kvargs["createdAt"]
            else:
                self_.createdAt = kvargs["createdAt"]
        if "createdBy" in kvargs:
            if type(kvargs["createdBy"]).__name__ is self_.__annotations__["createdBy"]:
                self_.createdBy = kvargs["createdBy"]
            else:
                self_.createdBy = kvargs["createdBy"]
        if "updatedAt" in kvargs:
            if type(kvargs["updatedAt"]).__name__ is self_.__annotations__["updatedAt"]:
                self_.updatedAt = kvargs["updatedAt"]
            else:
                self_.updatedAt = kvargs["updatedAt"]


@dataclass
class AssignmentCreate:
    """

    Attributes
    ----------
    assigneeId: str
      The userId or groupId based on the type.
    roles: list[str]
      The roles assigned to the assigneeId
    type: str
    """

    assigneeId: str = None
    roles: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):
        if "assigneeId" in kvargs:
            if (
                type(kvargs["assigneeId"]).__name__
                is self_.__annotations__["assigneeId"]
            ):
                self_.assigneeId = kvargs["assigneeId"]
            else:
                self_.assigneeId = kvargs["assigneeId"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]


@dataclass
class AssignmentUpdate:
    """

    Attributes
    ----------
    roles: list[str]
    """

    roles: list[str] = None

    def __init__(self_, **kvargs):
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]


@dataclass
class Assignments:
    """

    Attributes
    ----------
    data: list[Assignment]
    links: object
    meta: object
    """

    data: list[Assignment] = None
    links: object = None
    meta: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Assignment(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]


@dataclass
class FilterSpaces:
    """

    Attributes
    ----------
    ids: list[str]
    names: list[str]
    """

    ids: list[str] = None
    names: list[str] = None

    def __init__(self_, **kvargs):
        if "ids" in kvargs:
            if type(kvargs["ids"]).__name__ is self_.__annotations__["ids"]:
                self_.ids = kvargs["ids"]
            else:
                self_.ids = kvargs["ids"]
        if "names" in kvargs:
            if type(kvargs["names"]).__name__ is self_.__annotations__["names"]:
                self_.names = kvargs["names"]
            else:
                self_.names = kvargs["names"]


@dataclass
class RawSpace:
    """

    Attributes
    ----------
    disabled: bool
    id: str
      The unique ID of the space.
    ownerId: str
      The user ID of the space owner.
    roles: list[str]
      The list of roles assigned to the current user.
    type: str
      The type of the space.
    """

    disabled: bool = None
    id: str = None
    ownerId: str = None
    roles: list[str] = None
    type: str = None

    def __init__(self_, **kvargs):
        if "disabled" in kvargs:
            if type(kvargs["disabled"]).__name__ is self_.__annotations__["disabled"]:
                self_.disabled = kvargs["disabled"]
            else:
                self_.disabled = kvargs["disabled"]
        if "id" in kvargs:
            if type(kvargs["id"]).__name__ is self_.__annotations__["id"]:
                self_.id = kvargs["id"]
            else:
                self_.id = kvargs["id"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]
        if "roles" in kvargs:
            if type(kvargs["roles"]).__name__ is self_.__annotations__["roles"]:
                self_.roles = kvargs["roles"]
            else:
                self_.roles = kvargs["roles"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]


@dataclass
class RawSpaces:
    """

    Attributes
    ----------
    data: list[RawSpace]
    """

    data: list[RawSpace] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [RawSpace(**e) for e in kvargs["data"]]


@dataclass
class RawSpacesCompressed:
    """

    Attributes
    ----------
    data: object
    """

    data: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]


@dataclass
class SpaceCreate:
    """

    Attributes
    ----------
    name: str
      The name of the space. Personal spaces do not have a name.
    type: str
    description: str
      The description of the space. Personal spaces do not have a description.
    """

    name: str = None
    type: str = None
    description: str = None

    def __init__(self_, **kvargs):
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "type" in kvargs:
            if type(kvargs["type"]).__name__ is self_.__annotations__["type"]:
                self_.type = kvargs["type"]
            else:
                self_.type = kvargs["type"]
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]


@dataclass
class SpacePatch(dict):
    """

    Attributes
    ----------
    """

    def __init__(self_, **kvargs):
        pass


@dataclass
class SpaceTypes:
    """
    The distinct types of spaces (shared, managed, etc)

    Attributes
    ----------
    data: list[str]
    """

    data: list[str] = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = kvargs["data"]


@dataclass
class SpaceUpdate:
    """

    Attributes
    ----------
    description: str
      The description of the space. Personal spaces do not have a description.
    name: str
    ownerId: str
      The user id of the space owner.
    """

    description: str = None
    name: str = None
    ownerId: str = None

    def __init__(self_, **kvargs):
        if "description" in kvargs:
            if (
                type(kvargs["description"]).__name__
                is self_.__annotations__["description"]
            ):
                self_.description = kvargs["description"]
            else:
                self_.description = kvargs["description"]
        if "name" in kvargs:
            if type(kvargs["name"]).__name__ is self_.__annotations__["name"]:
                self_.name = kvargs["name"]
            else:
                self_.name = kvargs["name"]
        if "ownerId" in kvargs:
            if type(kvargs["ownerId"]).__name__ is self_.__annotations__["ownerId"]:
                self_.ownerId = kvargs["ownerId"]
            else:
                self_.ownerId = kvargs["ownerId"]


@dataclass
class SpacesClass:
    """

    Attributes
    ----------
    data: list[Space]
    links: object
    meta: object
    """

    data: list[Space] = None
    links: object = None
    meta: object = None

    def __init__(self_, **kvargs):
        if "data" in kvargs:
            if type(kvargs["data"]).__name__ is self_.__annotations__["data"]:
                self_.data = kvargs["data"]
            else:
                self_.data = [Space(**e) for e in kvargs["data"]]
        if "links" in kvargs:
            if type(kvargs["links"]).__name__ is self_.__annotations__["links"]:
                self_.links = kvargs["links"]
            else:
                self_.links = kvargs["links"]
        if "meta" in kvargs:
            if type(kvargs["meta"]).__name__ is self_.__annotations__["meta"]:
                self_.meta = kvargs["meta"]
            else:
                self_.meta = kvargs["meta"]


@dataclass
class SpacesSettings:
    """
    Space specific settings.

    Attributes
    ----------
    allowOffline: bool
    allowShares: bool
    """

    allowOffline: bool = None
    allowShares: bool = None

    def __init__(self_, **kvargs):
        if "allowOffline" in kvargs:
            if (
                type(kvargs["allowOffline"]).__name__
                is self_.__annotations__["allowOffline"]
            ):
                self_.allowOffline = kvargs["allowOffline"]
            else:
                self_.allowOffline = kvargs["allowOffline"]
        if "allowShares" in kvargs:
            if (
                type(kvargs["allowShares"]).__name__
                is self_.__annotations__["allowShares"]
            ):
                self_.allowShares = kvargs["allowShares"]
            else:
                self_.allowShares = kvargs["allowShares"]


@dataclass
class SpacesSettingsUpdate:
    """

    Attributes
    ----------
    allowOffline: bool
    allowShares: bool
    """

    allowOffline: bool = None
    allowShares: bool = None

    def __init__(self_, **kvargs):
        if "allowOffline" in kvargs:
            if (
                type(kvargs["allowOffline"]).__name__
                is self_.__annotations__["allowOffline"]
            ):
                self_.allowOffline = kvargs["allowOffline"]
            else:
                self_.allowOffline = kvargs["allowOffline"]
        if "allowShares" in kvargs:
            if (
                type(kvargs["allowShares"]).__name__
                is self_.__annotations__["allowShares"]
            ):
                self_.allowShares = kvargs["allowShares"]
            else:
                self_.allowShares = kvargs["allowShares"]


class Spaces:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.auth = Auth(config)

    def get_spaces(
        self,
        max_items=10,
        type: str = None,
        action: str = None,
        sort: str = None,
        name: str = None,
        ownerId: str = None,
        limit: int = None,
        next: str = None,
        prev: str = None,
    ) -> ListableResource[Space]:
        """
        Deprecated
        Retrieves spaces that the current user has access to and match the query.


        type: str
          Type(s) of space to filter. For example, "?type=managed,shared".

        action: str
          Action on space. For example, "?action=publish".

        sort: str
          Field to sort by. Prefix with +/- to indicate asc/desc. For example, "?sort=+name" to sort ascending on Name. Supported fields are "type", "name" and "createdAt".

        name: str
          Space name to search and filter for. Case insensitive open search with wildcards both as prefix and suffix. For example, "?name=fin" will get "finance", "Final" and "Griffin".

        ownerId: str
          Space ownerId to filter by. For example, "?ownerId=123".

        limit: int
          Max number of spaces to return.

        next: str
          The next page cursor. Next links make use of this.

        prev: str
          The previous page cursor. Previous links make use of this.

        Parameters
        ----------
        type: str = None
        action: str = None
        sort: str = None
        name: str = None
        ownerId: str = None
        limit: int = None
        next: str = None
        prev: str = None
        """
        warnings.warn("get_spaces is deprecated", DeprecationWarning, stacklevel=2)
        query_params = {}
        if type is not None:
            query_params["type"] = type
        if action is not None:
            query_params["action"] = action
        if sort is not None:
            query_params["sort"] = sort
        if name is not None:
            query_params["name"] = name
        if ownerId is not None:
            query_params["ownerId"] = ownerId
        if limit is not None:
            query_params["limit"] = limit
        if next is not None:
            query_params["next"] = next
        if prev is not None:
            query_params["prev"] = prev

        response = self.auth.rest(
            path="/spaces",
            method="GET",
            params=query_params,
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces",
            max_items=max_items,
            query_params=query_params,
        )

    def create(self, body: SpaceCreate) -> Space:
        """
        Deprecated
        Creates a space


        Parameters
        ----------
        body: SpaceCreate
        """
        warnings.warn("create is deprecated", DeprecationWarning, stacklevel=2)

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces",
            method="POST",
            params={},
            data=data,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj

    def create_filters(
        self, body: FilterSpaces, max_items=10
    ) -> ListableResource[Space]:
        """
        Deprecated
        Experimental
        Retrieves spaces that the current user has access to with provided space IDs or names.


        Parameters
        ----------
        body: FilterSpaces
        """
        warnings.warn("create_filters is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("create_filters is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces/filter",
            method="POST",
            params={},
            data=data,
        )
        return ListableResource(
            response=response.json(),
            cls=Space,
            auth=self.auth,
            path="/spaces/filter",
            max_items=max_items,
            query_params={},
        )

    def get_raw(self) -> RawSpacesCompressed:
        """
        Deprecated
        Experimental
        Retrieves compressed raw spaces of the current user.
        Retrieve compressed raw spaces of the current user.

        This endpoint only returns the spaces that the current user has assignments in.

        It returns the minimum amount of information to characterize the assignments of the current user per space.

        Response includes all space types: shared, managed and data.


        Parameters
        ----------
        """
        warnings.warn("get_raw is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("get_raw is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/raw",
            method="GET",
            params={},
            data=None,
        )
        obj = RawSpacesCompressed(**response.json())
        obj.auth = self.auth
        return obj

    def get_raw_spaces(self, max_items=10) -> ListableResource[RawSpace]:
        """
        Deprecated
        Retrieves raw spaces of the current user.
        Retrieve raw spaces of the current user.

        This endpoint only returns the spaces that the current user has assignments in.

        It returns the minimum amount of information to characterize the assignments of the current user per space.

        Response includes all space types: shared and managed.


        Parameters
        ----------
        """
        warnings.warn("get_raw-spaces is deprecated", DeprecationWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/raw-spaces",
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=RawSpace,
            auth=self.auth,
            path="/spaces/raw-spaces",
            max_items=max_items,
            query_params={},
        )

    def get_settings(self) -> SpacesSettings:
        """
        Deprecated
        Experimental
        Space-specific settings. For example, 'allowOffline' to allow offline usage from shared or managed spaces.


        Parameters
        ----------
        """
        warnings.warn("get_settings is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("get_settings is experimental", UserWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/settings",
            method="GET",
            params={},
            data=None,
        )
        obj = SpacesSettings(**response.json())
        obj.auth = self.auth
        return obj

    def set_settings(self, body: SpacesSettingsUpdate) -> SpacesSettings:
        """
        Deprecated
        Experimental
        Upserts space-specific settings.


        Parameters
        ----------
        body: SpacesSettingsUpdate
        """
        warnings.warn("set_settings is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("set_settings is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces/settings",
            method="PUT",
            params={},
            data=data,
        )
        obj = SpacesSettings(**response.json())
        obj.auth = self.auth
        return obj

    def get_types(self, max_items=10) -> ListableResource[String]:
        """
        Deprecated
        Gets a list of distinct space types.


        Parameters
        ----------
        """
        warnings.warn("get_types is deprecated", DeprecationWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/types",
            method="GET",
            params={},
            data=None,
        )
        return ListableResource(
            response=response.json(),
            cls=String,
            auth=self.auth,
            path="/spaces/types",
            max_items=max_items,
            query_params={},
        )

    def get(self, spaceId: str) -> Space:
        """
        Deprecated
        Retrieves a single space by ID.


        spaceId: str
          The ID of the space to retrieve.

        Parameters
        ----------
        spaceId: str
        """
        warnings.warn("get is deprecated", DeprecationWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/{spaceId}".replace("{spaceId}", spaceId),
            method="GET",
            params={},
            data=None,
        )
        obj = Space(**response.json())
        obj.auth = self.auth
        return obj

    def delete_assignment(self, spaceId: str, assignmentId: str) -> None:
        """
        Deprecated
        Deletes an assignment.


        spaceId: str
          The ID of the space of the assignment.

        assignmentId: str
          The ID of the assignment to delete.

        Parameters
        ----------
        spaceId: str
        assignmentId: str
        """
        warnings.warn(
            "delete_assignment is deprecated", DeprecationWarning, stacklevel=2
        )

        self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{spaceId}", spaceId
            ).replace("{assignmentId}", assignmentId),
            method="DELETE",
            params={},
            data=None,
        )

    def get_assignment(self, spaceId: str, assignmentId: str) -> Assignment:
        """
        Deprecated
        Retrieves a single assignment by ID.


        spaceId: str
          The ID of the space of the assignment.

        assignmentId: str
          The ID of the assignment to retrieve.

        Parameters
        ----------
        spaceId: str
        assignmentId: str
        """
        warnings.warn("get_assignment is deprecated", DeprecationWarning, stacklevel=2)

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{spaceId}", spaceId
            ).replace("{assignmentId}", assignmentId),
            method="GET",
            params={},
            data=None,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj

    def set_assignment(
        self, spaceId: str, assignmentId: str, body: AssignmentUpdate
    ) -> Assignment:
        """
        Deprecated
        Experimental
        Updates a single assignment by ID. The complete list of roles must be provided.


        spaceId: str
          The ID of the space of the assignment.

        assignmentId: str
          The ID of the assignment to update.

        Parameters
        ----------
        spaceId: str
        assignmentId: str
        body: AssignmentUpdate
        """
        warnings.warn("set_assignment is deprecated", DeprecationWarning, stacklevel=2)
        warnings.warn("set_assignment is experimental", UserWarning, stacklevel=2)

        try:
            data = asdict(body)
        except:
            data = body

        response = self.auth.rest(
            path="/spaces/{spaceId}/assignments/{assignmentId}".replace(
                "{spaceId}", spaceId
            ).replace("{assignmentId}", assignmentId),
            method="PUT",
            params={},
            data=data,
        )
        obj = Assignment(**response.json())
        obj.auth = self.auth
        return obj
