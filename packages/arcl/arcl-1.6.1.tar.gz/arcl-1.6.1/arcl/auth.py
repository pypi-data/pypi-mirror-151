import json
import os

import click
import msal
import requests

from .config import get_config_path, get_api_config, get_token_path, ARCHIMEDES_CONF_DIR
from .token_cache import get_token_cache

AUTH_ACTIONS_LOGIN = "login"
AUTH_ACTIONS_LOGOUT = "logout"
AUTH_ACTIONS_GET_TOKEN = "get-token"
AUTH_ACTIONS = [
    AUTH_ACTIONS_LOGIN,
    AUTH_ACTIONS_LOGOUT,
    AUTH_ACTIONS_GET_TOKEN,
]


class ArchimedesAuth:
    def __init__(self, env):
        self.env = env
        self.saved_config_path = get_config_path(env)
        self.token_path = get_token_path(env)
        self.api_config = get_api_config(self.env)
        self.app = self.build_msal_app(
            self.api_config.client_id, cache=get_token_cache(env)
        )

    def get_scopes(self):
        return [
            f"api://{self.api_config.aad_app_client_id}/.default",
        ]

    def get_access_token_silent(self):
        # We now check the cache to see
        # whether we already have some accounts that the end user already used to sign in before.
        accounts = self.app.get_accounts()
        if not accounts:
            return None

        chosen = accounts[0]
        result = self.app.acquire_token_silent(self.get_scopes(), account=chosen)

        if result is None or "access_token" not in result:
            click.echo("Could not get access token silently")

            if result is not None:
                click.echo(result.get("error"))
                click.echo(result.get("error_description"))

            return None

        return result.get("access_token")

    def get_access_token_by_device_flow(self):
        flow = self.app.initiate_device_flow(self.get_scopes())
        message = flow.get("message")
        click.echo(message)
        result = self.app.acquire_token_by_device_flow(flow)

        if result is None or "access_token" not in result:
            click.echo("Could not login. Try logging out and logging in again.")

            if result is not None:
                click.echo(result.get("error"))
                click.echo(result.get("error_description"))

            return None

        return result.get("access_token")

    def get_access_token(self):
        access_token = self.get_access_token_silent()
        if not access_token:
            access_token = self.get_access_token_by_device_flow()
        return access_token

    def login(self, organization_id):
        access_token = self.get_access_token()

        if organization_id is None:
            url = f"{self.api_config.url}/v2/config/"
        else:
            url = f"{self.api_config.url}/v1/config/{organization_id}/"

        try:
            page = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                },
            )
            page.raise_for_status()
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
            click.echo("Failed connecting to the server", e)
        except requests.exceptions.HTTPError:
            click.echo(page.content)
            contents = page.json()
            if "detail" in contents:
                click.echo(contents["detail"])
            else:
                click.echo(contents)
        else:
            config = page.json()
            config_json = json.dumps(config, indent=2)
            open(self.saved_config_path, "w").write(config_json)
            click.echo(f"Login successful into env: {self.env}")

    def logout(self):
        # remove older tokens created on previous versions
        for file_to_remove in (
            "arcl.json",
            "msal.cache.bin",
        ):
            try:
                os.remove(os.path.join(ARCHIMEDES_CONF_DIR, file_to_remove))
            except FileNotFoundError:
                pass

        if os.path.exists(self.saved_config_path):
            os.remove(self.saved_config_path)

        if os.path.exists(self.token_path):
            os.remove(self.token_path)

        click.echo(f"Logout successful from  env: {self.env}")

    def build_msal_app(self, client_id, cache=None):
        return msal.PublicClientApplication(
            client_id,
            authority=self.api_config.authority,
            token_cache=cache,
        )
