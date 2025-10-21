"""Plugin tests."""

import pytest

from cmem_plugin_parameters import ParametersPlugin

from .utils import TestExecutionContext, needs_cmem


@needs_cmem
def test_execution() -> None:
    """Test plugin execution"""
    context = TestExecutionContext()

    ParametersPlugin(parameters="key1: value").execute((), context)

    entities = ParametersPlugin(
        parameters="""key: value
x: y"""
    ).execute((), context)
    schema_path_length_before = 2
    value_length_before = 2
    assert len(entities.schema.paths) == schema_path_length_before
    assert len(entities.entities) == 1
    assert entities.entities[0].uri == "urn:x-eccenca:Parameter"
    assert len(entities.entities[0].values) == value_length_before
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
    schema_path_length_after = 4
    value_length_after = 4
    assert len(entities.schema.paths) == schema_path_length_after
    assert len(entities.entities) == 1
    assert entities.entities[0].uri == "urn:x-eccenca:Parameter"
    assert len(entities.entities[0].values) == value_length_after
    assert entities.entities[0].values[0][0] == "value3"


@needs_cmem
def test_execution_with_errors() -> None:
    """Test plugin execution"""
    context = TestExecutionContext()

    with pytest.raises(TypeError, match=r"We need at least one line 'key: value' here."):
        ParametersPlugin(parameters="one").execute((), context)

    with pytest.raises(TypeError, match=r"We need at least one line 'key: value' here."):
        ParametersPlugin(parameters="").execute((), context)

    with pytest.raises(TypeError, match=r"We need at least one line 'key: value' here."):
        ParametersPlugin(parameters="not,correct,parameter;key").execute((), context)

    with pytest.raises(ValueError, match=r"Error in parameter input:"):
        ParametersPlugin(
            parameters="""
key: value1
xxx
"""
        ).execute((), context)


def test_dummy() -> None:
    """Pytest raises ZeroDivisionError in case all tests are skipped"""
    assert 1 == 1  # noqa: PLR0133
