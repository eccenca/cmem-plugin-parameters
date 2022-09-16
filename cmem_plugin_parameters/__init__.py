"""Simple entities generation plugin to configure tasks in workflows."""
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
            name="parameter_settings",
            label="Parameter settings",
            description="Enter parameters and values in the form:"
                        " parameter[1],value[1];...;parameter[n],value[n]"
        )
    ]
)
class ParametersPlugin(WorkflowPlugin):

    def __init__(
            self,
            parameter_settings
    ) -> None:
        self.parameter_settings = parameter_settings

    def execute(self, inputs: Sequence[Entities],
                context: ExecutionContext) -> Entities:
        values = []
        paths = []
        for n in self.parameter_settings.split(";"):
            p, v = n.split(",")
            self.log.info(f"Parameter {p.strip()}: {v.strip()}")
            paths.append(EntityPath(path=p.strip()))
            values.append([v.strip()])
        entities = [Entity(uri="urn:Parameter", values=values)]
        return Entities(
            entities=entities,
            schema=EntitySchema(
                type_uri="urn:ParameterSettings",
                paths=paths
            )
        )
