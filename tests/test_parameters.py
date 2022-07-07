"""Plugin tests."""
from cmem_plugin_parameters import ParametersPlugin


def test_execution():
    """Test plugin execution"""

    plugin = ParametersPlugin(parameter_settings="")
    result = plugin.execute()


