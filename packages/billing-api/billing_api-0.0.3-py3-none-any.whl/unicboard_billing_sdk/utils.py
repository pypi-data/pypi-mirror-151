from typing import Dict, Any

from unicboard_billing_sdk.response_models import GetDeviceValueResponse, GetDeviceChannelValuePayloadResponse, \
    GetDeviceListInfoPayloadResponse, DataGatewayNetworkResponseModel, DeviceChannelResponseModel, NetworkResponseModel, \
    ProtokolResponseModel, DataGatewayResponseModel, DeviceManufacturerResponseModel, DeviceModificationResponseModel, \
    DeviceModificationTypeResponseModel, DeviceMeteringType, GetDeviceInfoResponse, GetDeviceListInfoResponse


def get_device_info_payload_structure(payload: Dict[str, Any]):
    data_gateway_network_device = payload.pop('data_gateway_network_device')
    network = data_gateway_network_device.pop('network')
    data_gateway = network.pop('data_gateway')
    protocol = data_gateway_network_device.pop('protocol')
    device_channels = payload.pop('device_channel')
    device_manufacturer = payload.pop('device_manufacturer')
    device_modification = payload.pop('device_modification')
    device_modification_type = device_modification.pop('device_modification_type')
    device_metering_type = device_modification_type.pop('device_metering_type')
    return GetDeviceListInfoPayloadResponse(
            **payload,
            data_gateway_network_device=DataGatewayNetworkResponseModel(
                **data_gateway_network_device,
                network=NetworkResponseModel(
                    **network,
                    data_gateway=DataGatewayResponseModel(**data_gateway),
                ),
                protocol=ProtokolResponseModel(**protocol),
            ),
            device_channel=[DeviceChannelResponseModel(**device_channel) for device_channel in device_channels],
            device_manufacturer=DeviceManufacturerResponseModel(**device_manufacturer),
            device_modification=DeviceModificationResponseModel(
                **device_modification,
                device_modification_type=DeviceModificationTypeResponseModel(
                    **device_modification_type,
                    device_metering_type=DeviceMeteringType(**device_metering_type)
                ),
            ),
        )


def get_device_info_structure(response: Dict[str, Any]) -> GetDeviceInfoResponse:
    payload = response.pop('payload')
    return GetDeviceInfoResponse(
        **response,
        payload=get_device_info_payload_structure(payload)
    )


def get_device_list_info_structure(response: Dict[str, Any]) -> GetDeviceListInfoResponse:
    payload = response.pop('payload')
    return GetDeviceListInfoResponse(
        **response,
        payload=[get_device_info_payload_structure(item) for item in payload]
    )


def get_device_value_structure(response: Dict[str, Any]) -> GetDeviceValueResponse:
    payload = response.pop('payload')
    return GetDeviceValueResponse(
        **response,
        payload=[GetDeviceChannelValuePayloadResponse(**item) for item in payload]
    )


