"""Module for the hub"""
from __future__ import annotations

from abc import ABC
from collections.abc import Callable
from datetime import datetime
import logging
from typing import Any

from slugify import slugify

import hahomematic.central_unit as hm_central
from hahomematic.const import (
    BACKEND_CCU,
    HUB_ADDRESS,
    INIT_DATETIME,
    SYSVAR_ADDRESS,
    HmEntityUsage,
    HmPlatform,
)
from hahomematic.helpers import HmDeviceInfo, generate_unique_id

_LOGGER = logging.getLogger(__name__)

EXCLUDED_FROM_SENSOR = [
    "pcCCUID",
]

EXCLUDED = [
    "OldVal",
]

SERVICE_MESSAGES = "Servicemeldungen"


class BaseHubEntity(ABC):
    """
    Base class for hub entities.
    """

    def __init__(
        self,
        central: hm_central.CentralUnit,
        unique_id: str,
        name: str,
        value: Any | None = None,
        unit: str | None = None,
    ):
        """
        Initialize the entity.
        """
        self._central = central
        self.unique_id = unique_id
        self.name = name
        self._value = value
        self._unit = unit
        self.last_update: datetime = INIT_DATETIME
        self._update_callbacks: list[Callable] = []
        self._remove_callbacks: list[Callable] = []
        self.create_in_ha: bool = True
        self.should_poll = False
        self.usage = HmEntityUsage.ENTITY

    @property
    def available(self) -> bool:
        """Return the availability of the device."""
        return self._central.available

    @property
    def device_information(self) -> HmDeviceInfo:
        """Return central specific attributes."""
        return self._central.device_information

    @property
    def attributes(self) -> dict[str, Any]:
        """Return the state attributes of the base entity."""
        return {}

    @property
    def platform(self) -> HmPlatform:
        """Return the platform."""
        return HmPlatform.HUB_SENSOR

    @property
    def value(self) -> Any:
        """Return the value of the entity."""
        return self._value

    @property
    def unit(self) -> str | None:
        """Return the unit of the entity."""
        if self._unit:
            return self._unit
        if isinstance(self._value, (int, float)):
            return "#"
        return None

    # pylint: disable=no-self-use
    async def load_data(self) -> None:
        """Do not load data for the hub here."""
        return

    # pylint: disable=no-self-use
    async def fetch_data(self) -> None:
        """fetch data for the hub."""
        return

    def register_update_callback(self, update_callback: Callable) -> None:
        """register update callback"""
        if callable(update_callback) and update_callback not in self._update_callbacks:
            self._update_callbacks.append(update_callback)

    def unregister_update_callback(self, update_callback: Callable) -> None:
        """remove update callback"""
        if update_callback in self._update_callbacks:
            self._update_callbacks.remove(update_callback)

    def update_entity(self, *args: Any) -> None:
        """
        Do what is needed when the state of the entity has been updated.
        """
        self._set_last_update()
        for _callback in self._update_callbacks:
            _callback(self.unique_id)

    def register_remove_callback(self, remove_callback: Callable) -> None:
        """register the remove callback"""
        if callable(remove_callback):
            self._remove_callbacks.append(remove_callback)

    def unregister_remove_callback(self, remove_callback: Callable) -> None:
        """remove the remove callback"""
        if remove_callback in self._remove_callbacks:
            self._remove_callbacks.remove(remove_callback)

    def remove_entity(self) -> None:
        """
        Do what is needed when the entity has been removed.
        """
        self._set_last_update()
        for _callback in self._remove_callbacks:
            _callback(self.unique_id)

    def _set_last_update(self) -> None:
        self.last_update = datetime.now()


class HmSystemVariable(BaseHubEntity):
    """Class for a homematic system variable."""

    def __init__(
        self, central: hm_central.CentralUnit, name: str, value: Any, unit: str | None
    ):
        self._hub: HmHub | None = central.hub
        unique_id = generate_unique_id(
            central=central,
            address=SYSVAR_ADDRESS,
            parameter=slugify(name),
        )
        super().__init__(
            central=central,
            unique_id=unique_id,
            name=f"{central.instance_name}_SV_{name}",
            value=value,
            unit=unit,
        )

    @property
    def device_information(self) -> HmDeviceInfo:
        """Return device specific attributes."""
        if self._hub:
            return self._hub.device_information
        return HmDeviceInfo(identifier="NN")

    @property
    def platform(self) -> HmPlatform:
        """Return the platform."""
        if isinstance(self.value, bool):
            return HmPlatform.HUB_BINARY_SENSOR
        return HmPlatform.HUB_SENSOR

    async def set_value(self, value: Any) -> None:
        """Set variable value on CCU/Homegear."""
        old_value = self._value
        if isinstance(old_value, bool):
            value = bool(value)
        elif isinstance(old_value, float):
            value = float(value)
        elif isinstance(old_value, int):
            value = int(value)
        elif isinstance(old_value, str):
            value = str(value)

        if self._value != value:
            self._value = value
            self.update_entity()


class HmHub(BaseHubEntity):
    """The HomeMatic hub. (CCU/HomeGear)."""

    def __init__(self, central: hm_central.CentralUnit):
        """Initialize HomeMatic hub."""
        unique_id: str = generate_unique_id(central=central, address=HUB_ADDRESS)
        name: str = central.instance_name
        super().__init__(central, unique_id, name)
        self.hub_entities: dict[str, HmSystemVariable] = {}
        self._variables: dict[str, Any] = {}
        self.should_poll = True

    @property
    def attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return self._variables.copy()

    @property
    def hub_entities_by_platform(self) -> dict[HmPlatform, list[HmSystemVariable]]:
        """Return the system variables by platform"""
        sysvars: dict[HmPlatform, list[HmSystemVariable]] = {}
        for entity in self.hub_entities.values():
            if entity.platform not in sysvars:
                sysvars[entity.platform] = []
            sysvars[entity.platform].append(entity)

        return sysvars

    async def fetch_data(self) -> None:
        """fetch data for the hub."""
        if self._central.available:
            await self._update_entities()
            await self._update_hub_state()

    async def _update_hub_state(self) -> None:
        """Retrieve latest service_messages."""
        value = 0
        if self._central.model == BACKEND_CCU:
            service_messages = await self._central.get_system_variable(SERVICE_MESSAGES)
            if service_messages is not None and isinstance(service_messages, float):
                value = int(service_messages)

        if self._value != value:
            self._value = value
            self.update_entity()

    async def _update_entities(self) -> None:
        """Retrieve all variable data and update hmvariable values."""
        self._variables.clear()
        variables = await self._central.get_all_system_variables()
        if not variables:
            _LOGGER.debug(
                "_update_entities: No sysvars received for %s",
                self._central.instance_name,
            )
            return
        _LOGGER.debug(
            "_update_entities: %i sysvars received for %s",
            len(variables),
            self._central.instance_name,
        )

        # remove some variables in case of CCU Backend
        # - OldValue(s) are for internal calculations
        if self._central.model is BACKEND_CCU:
            variables = _clean_variables(variables)

        for name, data in variables.items():
            value = data[0]
            unit = data[1]
            if _is_excluded(name, EXCLUDED_FROM_SENSOR):
                self._variables[name] = value
                continue

            entity: HmSystemVariable | None = self.hub_entities.get(name)
            if entity:
                await entity.set_value(value)
            else:
                self._create_system_variable(name, value, unit)

        self.update_entity()

    def _create_system_variable(self, name: str, value: Any, unit: str | None) -> None:
        """Create system variable as entity."""
        self.hub_entities[name] = HmSystemVariable(
            central=self._central,
            name=name,
            value=value,
            unit=unit,
        )

    async def set_system_variable(self, name: str, value: Any) -> None:
        """Set variable value on CCU/Homegear."""
        if name not in self.hub_entities:
            _LOGGER.warning("Variable %s not found on %s", name, self.name)
            return

        await self._central.set_system_variable(name, value)


def _is_excluded(variable: str, exclude_list: list[str]) -> bool:
    """Check if variable is excluded by exclude_list."""
    for marker in exclude_list:
        if marker in variable:
            return True
    return False


def _clean_variables(variables: dict[str, Any]) -> dict[str, Any]:
    cleaned_variables: dict[str, Any] = {}
    for name, value in variables.items():
        if _is_excluded(name, EXCLUDED):
            continue
        cleaned_variables[name] = value
    return cleaned_variables
