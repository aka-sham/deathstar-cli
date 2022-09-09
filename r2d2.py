#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Project          : deathstar-cli
# FileName         : r2d2.py
# -----------------------------------------------------------------------------
# Author           : Sébastien Metzger
# E-Mail           : sebastien.metzger@nomogi.org
##

import sys
import os
import logging
import logging.config
import fire
import requests

from requests import ConnectionError
from pathlib import Path
from pydantic import BaseModel
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable

from yaspin import yaspin
from yaspin.spinners import Spinners

# Logger
LOG = logging.getLogger("r2d2")


class Settings(BaseSettings):
    """Settings class to setup the CLI and configure logging."""

    backend_url: str

    class Config:
        """Overrides Config class to read .env file correctly."""

        env_file = ".env"
        env_file_encoding = "utf-8"

        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings, file_secret_settings

    def _get_exe_dir(self):
        """Gets Executable directory."""
        if "r2d2" in os.path.basename(sys.executable).lower():
            exe_dir = os.path.abspath(sys.executable)
        else:
            exe_dir = os.path.abspath(".")

        return exe_dir

    def init_logging(self):
        """Loads logging configuration file and inits logging system."""
        exe_dir = self._get_exe_dir()

        # Log directory
        log_dir = os.path.join(exe_dir, "logs")
        if not os.path.exists(log_dir):
            os.mkdir(log_dir)

        # Configuration file for logger
        log_file = os.path.join(exe_dir, "logging.conf")
        # Load configuration file
        logging.config.fileConfig(log_file)

        return logging.getLogger("r2d2")


class Mission(BaseModel):
    """Mission class which represents the response send from Millenium Falcon."""

    # Probability that the mission will succeed.
    probability: float


def ask_computer(millenium_falcon_settings: str, empire_settings: str):
    """
    Asks the Millenium Falcon computer to analyse if it is possible to save
    the targeted planet from the Death Star.

    Args:
        millenium_falcon_settings (str): Filepath to Millenium Falcon settings which describes, for instance, the targeted planet.
        empire_settings (str): Filepath to Empire settings which describes the countdown and the future location of bounty hunters.

    Returns:
        float: probability to save the targeted planet from the Death Star.
    """
    with yaspin(
        Spinners.moon,
        text="DrruurRRP tanaNDuh? Connection with Millenium Falcon initiated...",
    ) as sp:
        LOG.debug("Starts to communicate with Millenium Falcon...")

        millenium_falcon_settings_path = Path(millenium_falcon_settings)
        empire_settings_path = Path(empire_settings)

        if not millenium_falcon_settings_path.exists():
            LOG.fatal("Millenium Falcon settings file doesn't exist.")
            sp.text = "DrruurRRP tanaNDuh? Millenium Falcon settings file doesn't exist"
            sp.fail("💥")
            exit(1)

        if not empire_settings_path.exists():
            LOG.fatal("Empire settings file doesn't exist.")
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
            LOG.error("Cannot communicate with Millenium Falcon.")
            sp.text = "DrruurRRP tanaNDuh? Cannot communicate with Millenium Falcon."
            sp.fail("💥")
        else:
            # Retrieving mission probability
            mission = Mission.parse_raw(result.text, content_type="application/json")
            LOG.info(
                f"Millenium Falcon gave a result: you have {mission.probability:.2f}% of chance to save Endor!"
            )
            sp.text = f"WOOOAH twee-vwoop VRrrUHD DEda dah! You have {mission.probability:.2f}% of chance to save Endor!"
            sp.ok("✅")


# Application settings with default values
APP_SETTINGS = Settings(backend_url="http://127.0.0.1:8000")
APP_SETTINGS.init_logging()


if __name__ == "__main__":
    fire.Fire(ask_computer)

# EOF
