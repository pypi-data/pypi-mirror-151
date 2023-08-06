from typing import Any, Dict, Optional

from pydantic import BaseModel

from steamship.base import Client, Request
from steamship.base.response import Response
from steamship.data.plugin import (
    HostingCpu,
    HostingEnvironment,
    HostingMemory,
    HostingTimeout,
    HostingType,
)
from steamship.plugin.inputs.export_plugin_input import ExportPluginInput
from steamship.plugin.inputs.training_parameter_plugin_input import TrainingParameterPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.outputs.train_plugin_output import TrainPluginOutput
from steamship.plugin.outputs.training_parameter_plugin_output import TrainingParameterPluginOutput


class PluginInstance(BaseModel):
    client: Client = None
    id: str = None
    handle: str = None
    plugin_id: str = None
    plugin_version_id: str = None
    space_id: Optional[str] = None
    user_id: str = None
    config: Dict[str, Any] = None
    hosting_type: Optional[HostingType] = None
    hosting_cpu: Optional[HostingCpu] = None
    hosting_memory: Optional[HostingMemory] = None
    hosting_timeout: Optional[HostingTimeout] = None
    hosting_environment: Optional[HostingEnvironment] = None


class GetPluginInstanceRequest(Request):
    id: Optional[str] = None
    handle: Optional[str] = None


class CreatePluginInstanceRequest(Request):
    id: str = None
    pluginId: str = None
    pluginHandle: str = None
    pluginVersionId: str = None
    pluginVersionHandle: str = None
    handle: str = None
    upsert: bool = None
    config: Dict[str, Any] = None


class DeletePluginInstanceRequest(Request):
    id: str


class PluginInstance(BaseModel):
    client: Client = None
    id: str = None
    handle: str = None
    plugin_id: str = None
    plugin_version_id: str = None
    space_id: Optional[str] = None
    user_id: str = None
    config: Dict[str, Any] = None
    hosting_type: Optional[HostingType] = None
    hosting_cpu: Optional[HostingCpu] = None
    hosting_memory: Optional[HostingMemory] = None
    hosting_timeout: Optional[HostingTimeout] = None
    hosting_environment: Optional[HostingEnvironment] = None

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            handle=self.handle,
            pluginId=self.plugin_id,
            pluginVersionId=self.plugin_version_id,
            spaceId=self.space_id,
            userId=self.user_id,
            config=self.config,
            hostingType=self.hosting_type,
            hostingCpu=self.hosting_cpu,
            hostingMemory=self.hosting_memory,
            hostingTimeout=self.hosting_timeout,
            hostingEnvironment=self.hosting_environment,
        )

    @staticmethod
    def from_dict(d: Any, client: Client = None) -> PluginInstance:
        if "pluginInstance" in d:
            d = d["pluginInstance"]

        return PluginInstance(
            client=client,
            id=d.get("id"),
            handle=d.get("handle"),
            plugin_id=d.get("pluginId"),
            plugin_version_id=d.get("pluginVersionId"),
            config=d.get("config"),
            user_id=d.get("userId"),
            space_id=d.get("spaceId"),
            hosting_type=d.get("hostingType"),
            hosting_cpu=d.get("hostingCpu"),
            hosting_memory=d.get("hostingMemory"),
            hosting_timeout=d.get("hostingTimeout"),
            hosting_environment=d.get("hostingEnvironment"),
        )

    @staticmethod
    def create(
        client: Client,
        space_id: str = None,
        plugin_id: str = None,
        plugin_handle: str = None,
        plugin_version_id: str = None,
        plugin_version_handle: str = None,
        handle: str = None,
        upsert: bool = None,
        config: Dict[str, Any] = None,
    ) -> Response[PluginInstance]:
        req = CreatePluginInstanceRequest(
            handle=handle,
            pluginId=plugin_id,
            pluginHandle=plugin_handle,
            pluginVersionId=plugin_version_id,
            pluginVersionHandle=plugin_version_handle,
            upsert=upsert,
            config=config,
        )

        return client.post(
            "plugin/instance/create",
            payload=req,
            expect=PluginInstance,
            space_id=space_id,
        )

    @staticmethod
    def get(client: Client, handle: str):
        return client.post(
            "plugin/instance/get", GetPluginInstanceRequest(handle=handle), expect=PluginInstance
        )

    def delete(self) -> PluginInstance:
        req = DeletePluginInstanceRequest(id=self.id)
        return self.client.post("plugin/instance/delete", payload=req, expect=PluginInstance)

    def export(self, plugin_input: ExportPluginInput) -> Response[RawDataPluginOutput]:
        plugin_input.plugin_instance = self.handle
        return self.client.post(
            "plugin/instance/export", payload=plugin_input, expect=RawDataPluginOutput
        )

    def train(self, training_request: TrainingParameterPluginInput) -> Response[TrainPluginOutput]:
        return self.client.post(
            "plugin/instance/train", payload=training_request, expect=TrainPluginOutput
        )

    def get_training_parameters(
        self, training_request: TrainingParameterPluginInput
    ) -> Response[TrainingParameterPluginOutput]:
        return self.client.post(
            "plugin/instance/getTrainingParameters",
            payload=training_request,
            expect=TrainingParameterPluginOutput,
        )


class ListPrivatePluginInstancesRequest(Request):
    pass
