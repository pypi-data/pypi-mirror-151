import json
from typing import List
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .api import TopgreenerCloud

from . import util
from .capability import Capability
from .logger import logger
from .models import device_schema
from .models.meta_schema import MetaSchema
from .models.device_schema import DeviceSchema


class Device:
    schema: MetaSchema
    dev_schemas: List[DeviceSchema]
    capabilities: dict[Capability, DeviceSchema]

    def __init__(self, name: str, devId: str, gid: str, api: 'TopgreenerCloud'):
        self.api = api
        self.name = name
        self.devId = devId
        self.gid = gid
        self.capabilities = {}

    def set_schema(self, schema: MetaSchema):
        self.schema = schema
        self.dev_schemas = device_schema.deviceschemas_from_dict(json.loads(self.schema.schema_info.schema))
        self.capabilities.clear()
        for dev in self.dev_schemas:
            self.capabilities[dev.get_capability()] = dev

    def get_capabilities(self):
        abilities = []
        for capability in self.dev_schemas:
            abilities.append(capability.get_capability())

        return abilities

    async def set_power_state(self, state: bool):
        if Capability.SWITCH_LED in self.capabilities:
            # then we are good, because the capability exists to do this
            power_ability = self.capabilities[Capability.SWITCH_LED]
            dps = {power_ability.id: state}
            resp = await self.api.sendRequest('tuya.m.device.dp.publish', gid=self.gid,
                                              data={
                                                  "devId": self.devId,
                                                  "gwId": self.devId,
                                                  "dps": dps
                                              })
            logger.debug("Response to power is %s", resp)

    async def set_brightness(self, brightness: int):
        if Capability.BRIGHT_VALUE in self.capabilities:
            bright_ability = self.capabilities[Capability.BRIGHT_VALUE]
            min = bright_ability.property.min
            max = bright_ability.property.max

            nbright = util.scale_number(brightness, min, max, 0, 100)
            dps = {bright_ability.id: nbright}
            resp = await self.api.sendRequest('tuya.m.device.dp.publish', gid=self.gid,
                                              data={
                                                  "devId": self.devId,
                                                  "gwId": self.devId,
                                                  "dps": dps
                                              })
            logger.debug("Response to set brightness %s", resp)


