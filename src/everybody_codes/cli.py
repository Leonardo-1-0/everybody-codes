import os
import sys
from datetime import datetime
from functools import cache
from typing import Annotated

import requests
import typer
from dotenv import load_dotenv
from loguru import logger
from requests.exceptions import RequestException


class ECClient:
    endpoints: dict[str, str] = {
        "seed_number": "https://everybody.codes/api/user/me",
        "input": "https://everybody-codes.b-cdn.net/assets/{event}/{quest}/input/{seed}.json",
        "aes_keys": "https://everybody.codes/api/event/{event}/quest/{quest}",
    }

    def __init__(self) -> None:
        self.cookie: str | None = None
        self.user: str | None = None
        self.header: dict | None = None
        self.set_env()

    def set_env(self) -> None:
        logger.info("Setting environment.")

        load_dotenv()
        user = os.environ.get("EC_USER", None)
        if not user:
            logger.error(
                "User not found. Make sure the 'EC_USER' env variable is set before running the program."
            )
            sys.exit(1)
        self.user = user

        cookie = os.environ.get("EC_SESSION_COOKIE", None)
        if not cookie:
            logger.error(
                "Session cookie not found. Make sure the 'EC_SESSION_COOKIE' env variable is set before running the program."
            )
            sys.exit(1)
        self.cookie = cookie

        header = {
            "User-Agent": self.user,
            "Cookie": f"everybody-codes={self.cookie}",
        }
        self.header = header

    def _request(self, endpoint: str) -> dict:
        try:
            response = requests.get(endpoint)
            response.raise_for_status()
        except RequestException:
            raise
        return response.json()

    @logger.catch(message="Failed to fetch seed number.", level="ERROR")
    def _get_seed_number(self) -> int:
        logger.debug(self.header)
        endpoint = self.endpoints["seed_number"]
        logger.info(f"Fetching seed number from {endpoint}.")
        response = self._request(endpoint)
        logger.debug(response)
        return response["seed"]

    @logger.catch(message="Failed to fetch inputs.", level="ERROR")
    def _get_inputs(self, *, event: int, quest: int) -> None:
        seed: int = self._get_seed_number()
        endpoint = self.endpoints["input"].format(event=event, quest=quest, seed=seed)
        logger.info(f"Fetching inputs from {endpoint}.")
        response = self._request(endpoint)
        logger.debug(response)

    @logger.catch(message="Failed to fetch AES keys.", level="ERROR")
    def _get_aes_keys(self, *, event: int, quest: int) -> dict:
        endpoint = self.endpoints["aes_keys"].format(event=event, quest=quest)
        logger.info(f"Fetching AES keys from {endpoint}.")
        response = self._request(endpoint)
        logger.debug(response)
        if "key1" not in response:
            raise ValueError("")
        return response


@cache
def get_client() -> ECClient:
    return ECClient()


def get_seed_number() -> None:
    client: ECClient = get_client()
    client._get_seed_number()


def get_aes_keys(
    quest: Annotated[int, typer.Argument(help="Quest number")],
    year: Annotated[int, typer.Argument(help="Contest year")] = datetime.now().year,
) -> None:
    client: ECClient = get_client()
    client._get_aes_keys(event=year, quest=quest)


def get_inputs(
    quest: Annotated[int, typer.Argument(help="Quest number")],
    year: Annotated[int, typer.Argument(help="Contest year")] = datetime.now().year,
) -> None:
    client: ECClient = get_client()
    client._get_inputs(event=year, quest=quest)


app = typer.Typer(name="Everybody Codes", no_args_is_help=True)

app.command("get_seed_number")(get_seed_number)
app.command("get_inputs")(get_inputs)


def main():
    app()


if __name__ == "__main__":
    main()
