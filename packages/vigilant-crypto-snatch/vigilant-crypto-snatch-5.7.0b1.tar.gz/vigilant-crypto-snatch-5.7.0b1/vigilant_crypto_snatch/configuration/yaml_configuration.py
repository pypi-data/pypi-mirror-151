import datetime
import os
from typing import List
from typing import Optional

import dateutil.parser
import yaml

from ..configuration import Configuration
from ..core import AssetPair
from ..historical import CryptoCompareConfig
from ..marketplace import BitstampConfig
from ..marketplace import CCXTConfig
from ..marketplace import KrakenConfig
from ..marketplace import KrakenWithdrawalConfig
from ..notifications import NotifyRunConfig
from ..notifications import TelegramConfig
from ..paths import config_path
from ..triggers import TriggerSpec


class YamlConfiguration(Configuration):
    def __init__(self, path=config_path):
        if not os.path.isfile(path):
            raise RuntimeError(f"Please create the configuration file at {path}.")

        with open(path) as f:
            self._config = yaml.safe_load(f)

    def get_trigger_config(self) -> List[TriggerSpec]:
        return [parse_trigger_spec(entry) for entry in self._config["triggers"]]

    def get_polling_interval(self) -> int:
        return self._config["sleep"]

    def get_crypto_compare_config(self) -> CryptoCompareConfig:
        return CryptoCompareConfig(**self._config["cryptocompare"])

    def get_kraken_config(self) -> Optional[KrakenConfig]:
        if "kraken" not in self._config:
            return None
        return KrakenConfig(
            key=self._config["kraken"]["key"],
            secret=self._config["kraken"]["secret"],
            prefer_fee_in_base_currency=self._config["kraken"].get(
                "prefer_fee_in_base_currency", False
            ),
            withdrawal={
                coin: KrakenWithdrawalConfig(
                    coin=coin,
                    target=withdrawal_dict["target"],
                    fee_limit_percent=withdrawal_dict["fee_limit_percent"],
                )
                for coin, withdrawal_dict in self._config["kraken"]
                .get("withdrawal", {})
                .items()
            },
        )

    def get_bitstamp_config(self) -> Optional[BitstampConfig]:
        if "bitstamp" not in self._config:
            return None
        return BitstampConfig(**self._config["bitstamp"])

    def get_telegram_config(self) -> Optional[TelegramConfig]:
        if "telegram" not in self._config:
            return None
        return TelegramConfig(**self._config["telegram"])

    def get_ccxt_config(self) -> CCXTConfig:
        return CCXTConfig(**self._config["ccxt"])

    def get_marketplace(self) -> str:
        return self._config.get("marketplace", "kraken")

    def get_notify_run_config(self) -> Optional[NotifyRunConfig]:
        if "notify_run" not in self._config:
            return None
        return NotifyRunConfig(**self._config["notify_run"])


def parse_trigger_spec(trigger_spec_dict: dict) -> TriggerSpec:
    cooldown_minutes = get_minutes(trigger_spec_dict, "cooldown")
    if cooldown_minutes is None:
        raise RuntimeError(f"Trigger needs to have a cooldown: {trigger_spec_dict}")

    trigger_spec = TriggerSpec(
        asset_pair=AssetPair(
            coin=trigger_spec_dict["coin"].upper(),
            fiat=trigger_spec_dict["fiat"].upper(),
        ),
        delay_minutes=get_minutes(trigger_spec_dict, "delay"),
        cooldown_minutes=cooldown_minutes,
        drop_percentage=trigger_spec_dict.get("drop_percentage", None),
        volume_fiat=trigger_spec_dict.get("volume_fiat", None),
        percentage_fiat=trigger_spec_dict.get("percentage_fiat", None),
        name=trigger_spec_dict.get("name", None),
        start=get_start(trigger_spec_dict),
        fear_and_greed_index_below=trigger_spec_dict.get(
            "fear_and_greed_index_below", None
        ),
    )

    return trigger_spec


def get_start(trigger_spec_dict: dict) -> Optional[datetime.datetime]:
    if "start" in trigger_spec_dict:
        start = trigger_spec_dict["start"]
        print(trigger_spec_dict)
        if isinstance(start, datetime.date):
            return datetime.datetime.combine(start, datetime.datetime.min.time())
        elif isinstance(start, str):
            return dateutil.parser.parse(start)
        else:
            raise RuntimeError(f"Cannot interpret date {start}")
    else:
        return None


def get_minutes(config: dict, key: str) -> Optional[int]:
    if f"{key}_days" in config:
        return config[f"{key}_days"] * 60 * 24
    if f"{key}_hours" in config:
        return config[f"{key}_hours"] * 60
    elif f"{key}_minutes" in config:
        return config[f"{key}_minutes"]
    else:
        return None
