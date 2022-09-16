"""Entities generation plugin to configure tasks in workflows."""
from typing import Sequence

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import Plugin, PluginParameter
from cmem_plugin_base.dataintegration.entity import (
    Entities, Entity, EntitySchema, EntityPath,
)
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin


@Plugin(
    label="Parameter Settings",
    description="Generates parameters and parameter settings.",
    documentation="""TBD""",
    parameters=[
        PluginParameter(
            name="parameters",
            label="Parameter settings",
            description="Enter parameters and values in the form:"
                        " parameter[1],value[1];...;parameter[n],value[n]"
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
