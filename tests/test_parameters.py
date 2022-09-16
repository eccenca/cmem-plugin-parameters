"""Plugin tests."""
import pytest

from cmem_plugin_parameters import ParametersPlugin
from .utils import TestExecutionContext


def test_execution():
    """Test plugin execution"""
    context = TestExecutionContext()

    with pytest.raises(Exception):
        ParametersPlugin(parameter_settings="").execute((), context)
