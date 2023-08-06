from datetime import datetime
from typing import NamedTuple, List, Any, Optional
from uuid import UUID


class DataGatewayResponseModel(NamedTuple):
    name: str


class NetworkResponseModel(NamedTuple):
    data_gateway: DataGatewayResponseModel
    name: str
    type_network: str


class ProtokolResponseModel(NamedTuple):
    name: str


class DataGatewayNetworkResponseModel(NamedTuple):
    network: NetworkResponseModel
    protocol: ProtokolResponseModel
    mac: int


class DeviceChannelResponseModel(NamedTuple):
    inactivity_limit: int
    last_date_event_no_data: Optional[datetime]
    last_value: Optional[float]
    last_value_date: Optional[datetime]
    serial_number: int
    unit_multiplier: float
    value_multiplier: float


class DeviceManufacturerResponseModel(NamedTuple):
    name: str


class DeviceMeteringType(NamedTuple):
    name_en: str
    name_ru: str
    sys_name: str


class DeviceModificationTypeResponseModel(NamedTuple):
    device_metering_type: DeviceMeteringType
    name_en: str
    name_ru: str
    sys_name: str
    type: str


class DeviceModificationResponseModel(NamedTuple):
    device_modification_type: DeviceModificationTypeResponseModel
    name: str


class GetDeviceListInfoPayloadResponse(NamedTuple):
    data_gateway_network_device: DataGatewayNetworkResponseModel
    device_channel: List[DeviceChannelResponseModel]
    device_manufacturer: DeviceManufacturerResponseModel
    device_modification: DeviceModificationResponseModel
    date_produced: datetime
    firmware_version: Optional[str]
    hardware_version: Optional[str]
    id: UUID
    manufacturer_serial_number: str


class GetDeviceListInfoResponse(NamedTuple):
    count: int
    errors: List[Any]
    ok: bool
    total_count: int
    payload: List[GetDeviceListInfoPayloadResponse]


class GetDeviceInfoResponse(NamedTuple):
    errors: List[Any]
    ok: bool
    payload: GetDeviceListInfoPayloadResponse


class GetDeviceChannelValuePayloadResponse(NamedTuple):
    channel_number: int
    date: datetime
    date_created: datetime
    device_id: UUID
    value: Optional[float]
    value_raw: Optional[float]
    value_type: str


class GetDeviceValueResponse(NamedTuple):
    count: int
    errors: List[Any]
    ok: bool
    total_count: int
    payload: List[GetDeviceChannelValuePayloadResponse]
