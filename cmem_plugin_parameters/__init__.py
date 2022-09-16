"""Entities generation plugin to configure tasks in workflows."""
from typing import Sequence

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities, Entity, EntitySchema, EntityPath,
)
from cmem_plugin_base.dataintegration.parameter.multiline import MultilineStringParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin

DESCRIPTION = """Connect this task to a config port of another task in order to set
or overwrite the parameter values of this task."""

DOCUMENTATION = f"""{DESCRIPTION}"""


@Plugin(
    label="Set or overwrite parameter values",
    plugin_id="cmem_plugin_parameters-ParametersPlugin",
    description=DESCRIPTION,
    documentation=DOCUMENTATION,
    parameters=[
        PluginParameter(
            name="parameters",
            label="Parameter Configuration",
            param_type=MultilineStringParameterType(),
            description="TBD"
        )
    ]
)
class ParametersPlugin(WorkflowPlugin):
    """Entities generation plugin to configure tasks in workflows."""

    def __init__(
            self,
            parameters
    ) -> None:
        self.parameter_settings = parameters

    def execute(self, inputs: Sequence[Entities],
                context: ExecutionContext) -> Entities:
        values = []
        paths = []
        for parameter in self.parameter_settings.split(";"):
            key, value = parameter.split(",")
            key = key.strip()
            value = value.strip()
            self.log.info(f"Parameter {key}: {value}")
            paths.append(EntityPath(path=key))
            values.append([value])
        entities = [
            Entity(uri="urn:Parameter", values=values)
        ]
        return Entities(
            entities=entities,
            schema=EntitySchema(
                type_uri="urn:ParameterSettings",
                paths=paths
            )
        )
