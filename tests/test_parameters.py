"""Plugin tests."""
import pytest

from cmem_plugin_parameters import ParametersPlugin

from .utils import TestExecutionContext


def test_execution():
    """Test plugin execution"""
    context = TestExecutionContext()

    ParametersPlugin(parameters="key1: value").execute((), context)

    entities = ParametersPlugin(parameters="""key: value
x: y""").execute((), context)
    assert len(entities.schema.paths) == 2
    assert len(entities.entities) == 1
    assert entities.entities[0].uri == 'urn:Parameter'
    assert len(entities.entities[0].values) == 2
    parameters = """
p2: value2
top:
  sub1: sub
  sub2:
    - a
    - 1
    - 1.3
    - True
p2: value3
# comments are fine as well
p1: value1
multi: |
    SELECT ?s
    WHERE ...
p3: test
    """
    entities = ParametersPlugin(parameters=parameters).execute((), context)
    assert len(entities.schema.paths) == 4
    assert len(entities.entities) == 1
    assert entities.entities[0].uri == 'urn:Parameter'
    assert len(entities.entities[0].values) == 4
    assert entities.entities[0].values[0][0] == 'value3'


def test_execution_with_errors():
    """Test plugin execution"""
    context = TestExecutionContext()

    with pytest.raises(ValueError) as e_info:
        ParametersPlugin(parameters="one").execute((), context)

    with pytest.raises(ValueError) as e_info:
        ParametersPlugin(parameters="").execute((), context)

    with pytest.raises(ValueError) as e_info:
        ParametersPlugin(parameters="not,correct,parameter;key").execute((), context)

    with pytest.raises(ValueError) as e_info:
        ParametersPlugin(parameters="""
key: value1
xxx
""").execute((), context)
