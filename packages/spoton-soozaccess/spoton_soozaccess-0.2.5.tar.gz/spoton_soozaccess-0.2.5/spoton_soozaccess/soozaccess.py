import json
from typing import Tuple

import requests
from requests import Response
from requests.exceptions import HTTPError

from .logger import Logger


class SoozAccess(object):
    host = ""
    verbose = None

    def __init__(self, name: str, token: str, force_create: bool = True):
        if SoozAccess.host == "":
            raise ValueError(
                "Please provide a host before instanciating with 'SoozAccess.host=\"http://<host>\"'"
            )
        if SoozAccess.verbose == None:
            raise ValueError(
                "Please provide a boolean value to 'verbose' attribute before instanciating"
            )

        self.name = name
        self.token = token
        self.force_create = force_create
        self.session = requests.session()
        Logger.display = SoozAccess.verbose

    def __enter__(self):
        _, r = self.login()
        if r.status_code == 200:
            return self

        if not self.force_create:
            return None

        _, r = self.create_user()

        if r.status_code == 200:
            self.login()
            return self

        return None

    def __exit__(self, *args, **kwargs):
        self.logout()

    @property
    def user_id(self):
        _, r = self.login()
        if r.status_code == 200:
            id = json.loads(r.content.decode("utf-8"))["id"]
            r = self.logout()
            return id

        _, r = self.post_user()
        if r.status_code == 200:
            id = json.loads(r.content.decode("utf-8"))["id"]
            return id

        return None

    # ENTERPRISE
    def post_enterprise(self, name: str):
        """Create an enterprise."""

        content = {"name": name}

        try:
            r = self.session.post(
                f"{SoozAccess.host}/enterprises", json=content
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Post Enterprise", r)

        return content, r

    def get_enterprise_factors(self, enterprise_id: int):
        """Get all factors with selected factors of an enterprise."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/enterprises/{enterprise_id}/factors")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Enterprise Factors", r)

        return content, r

    def put_entreprise_factors(self, enterprise: int):
        """Purge and recreate selected factors of an enterprise."""        
        raise NotImplementedError("Not implemented yet")

    # FACTORS
    def get_factors(self, theme: int) -> Tuple[dict, Response]:
        """Get all factors for a theme (not specific to an enterprise)."""
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes/{theme}/factors")
            r.raise_for_status()
        except HTTPError as e:
            SoozAccess.show_error(e)
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Factor", r)

        return content, r

    # GROUP MEMBERS
    def get_invitable_users(self, group: int):
        """Return users that can be invited to a group."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/groups/{group}/invitableUsers")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Invitable Users", r)

        return content, r

    def post_group_invite(self, group: int, ids: list[int]) -> Tuple[dict, Response]:
        """Invite users to a specific group."""
        content = {"userIds": ids}

        try:
            r = self.session.post(
                f"{SoozAccess.host}/groups/{group}/invite", json=content
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Invite to Group", r)

        return content, r

    def put_group_invitation(
        self, group: int, status: str = "accepted"
    ) -> Tuple[dict, Response]:
        """Accept/decline an invitation to join a group."""

        content = {"status": status}

        try:
            r = self.session.put(
                f"{SoozAccess.host}/groups/{group}/invitation", json=content
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status("    Accept Group Invitation", r)

        return {}, r

    def get_group_members(self, id: int):
        """Return members of a group."""
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/groups/{id}/members")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Groups Members", r)

        return content, r

    def delete_group_member(self, group: int, user: int):
        """Remove a user from a group."""

        content = {}

        try:
            r = self.session.delete(f"{SoozAccess.host}/groups/{group}/members/{user}")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Groups", r)

        return content, r

    # GROUPS
    def get_user_groups(self) -> Tuple[dict, Response]:
        """Returns all groups of a user."""
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/groups")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Groups", r)

        return content, r

    def post_group(self, name: str, description: str) -> Tuple[dict, Response]:
        """Create a group in the enterprise of the user."""
        if name in [g["group"]["name"] for g in self.get_groups()[0]]:
            Logger.write("Group already exists")
            return None, None

        content = {"name": name, "description": description}

        try:
            r = self.session.post(f"{SoozAccess.host}/groups", json=content)
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Insert Group", r)

        return content, r

    def put_group(self, group: int, name: str, description: str):
        """Update a group (requires the user to be admin of the group)."""

        content = {"name": name,"description": description,}

        try:
            r = self.session.put(
                f"{SoozAccess.host}/groups/{group}", json=content
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status("    Put Group", r)

        return {}, r

    def delete_group(self, group: int) -> Tuple[dict, Response]:
        """Delete a group (requires the user to be admin of the group)."""
        if group not in [g["group"]["id"] for g in self.get_user_groups()[0]]:
            Logger.write("Group does not exist")
            return None

        try:
            r = self.session.delete(f"{SoozAccess.host}/groups/{group}")
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status("    Remove Group", r)

        return {}, r

    # LEVELS
    def get_levels(self):
        """Return the current level of the user for gamification. The points are increased by 25 with each PUT to the themes-responses endpoint."""
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/levels")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Levels", r)
        
        return content, r

    # RESPONSE OPTIONS
    def get_oneshot(self) -> Tuple[dict, Response]:
        """Gets the whole survey catalogue (themes, factors, responseOptions) of an enterprise."""
        content = {}
        try:
            r = self.session.get(f"{SoozAccess.host}/oneshot")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    One Shot", r)

        return content, r

    def get_factor_response_options(self, theme: int, factor: int):
        """Get all possible responses for a particular factor."""

        content = {}

        try:
            r = self.session.get(
                f"{SoozAccess.host}/themes/{theme}/factors/{factor}/responseOptions"
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Factor Response Options", r)

        return content, r

    def get_theme_response_options(self, theme: int):
        """Get the responseOptions to the quetsion of a theme."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes/{theme}/responseOptions")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Theme Response Options", r)

        return content, r

    # RESPONSES
    def get_responses(self) -> Tuple[dict, Response]:
        """Get all responses of the user for today."""
        content = {}
        try:
            r = self.session.get(f"{SoozAccess.host}/oneshot/responses")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Responses", r)

        return content, r

    def get_all_responses(self, since: str, to:str) -> Tuple[dict, Response]:
        """Get all responses of the user for a specific period of time."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/oneshot/responses/since/{since}/to/{to}")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get All Responses", r)

        return content, r

    def get_factor_responses(self, theme: int, factor: int):
        """Get the responses of the user for today to this factor and for the given period."""

        content = {}

        try:
            r = self.session.get(
                f"{SoozAccess.host}/themes/{theme}/factors/{factor}/responses"
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Factor Responses", r)
            
        return content, r

    def put_response(
        self, theme: int, factor: int, value: int, date: str
    ) -> Tuple[dict, Response]:
        """Insert the current response of the user for this factor. Key on the columns (userId, factorId, date, period). If date is not specified, it is set to today."""
        content = {
            "responseOptionId": value,
            "roomId": None,
            "period": "day",
            "date": date,
        }

        try:
            r = self.session.put(
                f"{SoozAccess.host}/themes/{theme}/factors/{factor}/responses",
                json=content,
            )
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Insert Response", r)

        return content, r

    def delete_response(self, theme: int, factor: int, response: int):
        """Delete the given response."""

        try:
            r = self.session.delete(
                f"{SoozAccess.host}/themes/{theme}/factors/{factor}/responses/{response}"
            )
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status("    Delete Response", r)

        return {}, r


    def get_all_themes_responses(self):
        """Get responses of today to all themes for the user."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes/responses")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get All Themes Responses", r)

        return content, r


    def get_theme_responses(self, theme: int):
        """Get todays response of the user for given theme (only used for the environment category question)."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes/{theme}/responses")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get All Themes Responses", r)

        return content, r

    def put_theme_response(self, theme: int):
        """Update the crrent response of the user. Key on the columns (userId, themeId, period, date)."""
        raise NotImplementedError("Not implemented yet")

    # STATISTICS
    def get_stats_lastvote(self):
        """Returns last vote."""
        raise NotImplementedError("Not implemented yet")

    def get_stats_response_count_for_factor(
        self,
        factor: int,
        startdate: str,
        enddate: str,
        roomId: int = None,
        group: int or list[int] = None,
    ):
        """Returns the number of responses per responseId for one factor."""


        raise NotImplementedError("Not implemented yet")

    def get_stats_days(
        self,
        factor: int,
        startdate: str,
        enddate: str,
        roomId: int = None,
        group: int or list[int] = None,
    ):
        """Returns statistics by day (and by period or not)."""
        raise NotImplementedError("Not implemented yet")

    def get_stats_months(
        self,
        factor: int,
        startdate: str,
        enddate: str,
        roomId: int = None,
        group: int or list[int] = None,
    ):
        """Returns statsitics by month (and by period)."""
        raise NotImplementedError("Not implemented yet")

    def get_stats_season(
        self,
        factor: int,
        startdate: str,
        enddate: str,
        roomId: int = None,
        group: int or list[int] = None,
    ):
        """Returns statistics by season."""
        raise NotImplementedError("Not implemented yet")

    def get_stats_themes_by_votes(
        self,
        startdate: str,
        enddate: str,
        roomId: int = None,
        group: int or list[int] = None,
    ):
        """Returns the themes ordered by the number of votes (descending)."""
        raise NotImplementedError("Not implemented yet")

    def get_stats_themes_by_feeling(
        self,
        startdate: str,
        enddate: str,
        roomId: int = None,
        group: int or list[int] = None,
    ):
        """Returns themes ordered by the average of the resonses (i.e. satisfaction)."""
        raise NotImplementedError("Not implemented yet")

    # THEMES
    def get_themes(self) -> Tuple[dict, Response]:
        """Get all themes (not specific to an enterprise)."""
        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Themes", r)

        return content, r

    def get_theme(self, theme: int):
        """Get a specific theme."""

        content = {}

        try:
            r = self.session.get(f"{SoozAccess.host}/themes/{theme}")
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Get Theme", r)

        return content, r

    # USERS
    def post_user(self, entreprise_id: int = 1) -> Tuple[dict, Response]:
        """Create a user."""
        content = {
            "firstName": self.name,
            "lastName": self.name,
            "sex": "m",
            "username": self.name,
            "email": f"{self.name}@test",
            "enterpriseId": entreprise_id,
            "token": self.token,
            "activatePopup": True,
            "points": 0,
        }
        try:
            r = self.session.post(f"{SoozAccess.host}/users", json=content)
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status("    Create User", r)

        return content, r

    def put_user(self):
        """Update the connected user."""
        raise NotImplementedError("Not implemented yet")

    def login(self) -> Tuple[dict, Response]:
        """Login a user."""
        content = {"user": {"identifier": self.name, "token": self.token}}

        try:
            r = self.session.post(f"{SoozAccess.host}/users/login", json=content)
            r.raise_for_status()
        except HTTPError as e:
            pass
        else:
            content = json.loads(r.content.decode("utf-8"))
        finally:
            self.show_status(f"*{self.name}* Login", r)

        return content, r

    def logout(self) -> Tuple[dict, Response]:
        """Logout the connected user."""
        try:
            r = self.session.post(f"{SoozAccess.host}/users/logout")
            r.raise_for_status()
        except HTTPError as e:
            pass
        finally:
            self.show_status(f"*{self.name}* Logout", r)

        return {}, r

    # OTHER
    def remove_groups(self):
        for g in self.get_groups()[0]:
            self.delete_group(g["group"]["id"])

    def show_status(self, text: str, r: Response):
        Logger.write(f"[{'API':10s}] {text:30s} [{r.status_code}] {r.reason}")

    @classmethod
    def prepare_users(cls, group_name: str, users: list[str]):
        id_list = [SoozAccess(name, name).user_id for name in users]

        # create group invitations from admin account
        with SoozAccess("admin_dev", "admin_dev") as admin:
            admin.remove_groups()

            content, _ = admin.post_group(group_name, "")
            group_id = content["groupId"]
            admin.post_group_invite(group_id, id_list)

        # accepts invitations from admin
        for name in users:
            with SoozAccess(name, name) as user:
                user.put_group_invitation(group_id)
