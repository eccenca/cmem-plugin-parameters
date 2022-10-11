"""Entities generation plugin to configure tasks in workflows."""
from typing import Sequence

from cmem_plugin_base.dataintegration.context import ExecutionContext
from cmem_plugin_base.dataintegration.description import (Plugin,
                                                          PluginParameter)
from cmem_plugin_base.dataintegration.entity import (Entities, Entity,
                                                     EntityPath, EntitySchema)
from cmem_plugin_base.dataintegration.parameter.multiline import \
    MultilineStringParameterType
from cmem_plugin_base.dataintegration.plugins import WorkflowPlugin
from yaml import safe_load, YAMLError

DESCRIPTION = """Connect this task to a config port of another task in order to set
or overwrite the parameter values of this task."""

DOCUMENTATION = f"""{DESCRIPTION}"""


def yaml_to_entities(yaml_string: str):
    """Generate entities from the yaml string."""
    parameters = safe_load(yaml_string)
    if not isinstance(parameters, dict):
        raise ValueError(
            "We need at least one line 'key: value' here."
        )
    values = []
    paths = []
    for key, value in parameters.items():
        if type(value) in (str, int, float, bool):
            paths.append(EntityPath(path=key))
            values.append([value])
    entities = [Entity(uri="urn:Parameter", values=values)]
    return Entities(
        entities=entities,
        schema=EntitySchema(type_uri="urn:ParameterSettings", paths=paths),
    )


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
            description="TBD",
        )
    ],
)
class ParametersPlugin(WorkflowPlugin):
    """Entities generation plugin to configure tasks in workflows."""

    def __init__(self, parameters) -> None:
        try:
            self.entities = yaml_to_entities(parameters)
        except YAMLError as error:
            raise ValueError(
                f"Error in parameter input: {str(error)}"
            ) from error

    def execute(
        self, inputs: Sequence[Entities], context: ExecutionContext
    ) -> Entities:
        return self.entities
