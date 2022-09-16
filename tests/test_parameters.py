"""Plugin tests."""
import pytest

from cmem_plugin_parameters import ParametersPlugin

from .utils import TestExecutionContext


def test_execution():
    """Test plugin execution"""
    context = TestExecutionContext()

    ParametersPlugin(parameters="key1,value1;key2,value2").execute((), context)


def test_execution_with_errors():
    """Test plugin execution"""
    context = TestExecutionContext()

    with pytest.raises(Exception):
        ParametersPlugin(parameters="").execute((), context)

    with pytest.raises(Exception):
        ParametersPlugin(parameters="not,correct,parameter;key").execute((), context)
