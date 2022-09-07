#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import fire
import requests

from requests import ConnectionError
from pathlib import Path
from pydantic import BaseModel
from pydantic import BaseSettings

from yaspin import yaspin
from yaspin.spinners import Spinners


class Settings(BaseSettings):
    backend_url: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Mission(BaseModel):
    probability: float


def ask_computer(millenium_falcon_settings: str, empire_settings: str):
    """
    Asks the Millenium Falcon computer to analyse if it is possible to save
    the targeted planet from the Death Star.

    Args:
        millenium_falcon_settings (_type_): Filepath to Millenium Falcon settings which describes, for instance, the targeted planet.
        empire_settings (_type_): Filepath to Empire settings which describes the countdown and the future location of bounty hunters.

    Returns:
        float: probability to save the targeted planet from the Death Star.
    """
    with yaspin(
        Spinners.moon,
        text="DrruurRRP tanaNDuh? Connection with Millenium Falcon initiated...",
    ) as sp:
        millenium_falcon_settings_path = Path(millenium_falcon_settings)
        empire_settings_path = Path(empire_settings)

        if not millenium_falcon_settings_path.exists():
            sp.text = "DrruurRRP tanaNDuh? Millenium Falcon settings file doesn't exist"
            sp.fail("💥")
            exit(1)

        if not empire_settings_path.exists():
            sp.text = "DrruurRRP tanaNDuh? Empire settings file doesn't exist"
            sp.fail("💥")
            exit(1)

        files = {
            "empire": open(empire_settings_path, "rb"),
            "millenium_falcon": open(millenium_falcon_settings_path, "rb"),
        }

        try:
            result = requests.post(f"{APP_SETTINGS.backend_url}/r2d2", files=files)
        except ConnectionError:
            sp.text = "DrruurRRP tanaNDuh? Cannot communicate with Millenium Falcon."
            sp.fail("💥")
        else:
            mission = Mission.parse_raw(result.text, content_type="application/json")
            sp.text = f"WOOOAH twee-vwoop VRrrUHD DEda dah! You have {mission.probability:.2f}% of chance to save Endor!"
            sp.ok("✅")


def main():
    fire.Fire(ask_computer)


# Application settings with default values
APP_SETTINGS = Settings(backend_url="http://127.0.0.1:8000")


if __name__ == "__main__":
    main()
