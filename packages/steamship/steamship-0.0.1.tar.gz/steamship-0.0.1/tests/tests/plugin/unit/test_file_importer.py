import base64

import pytest

from steamship.app import Response
from steamship.data.file import File
from steamship.plugin.inputs.train_plugin_input import TrainPluginInput
from steamship.plugin.inputs.training_parameter_plugin_input import TrainingParameterPluginInput
from steamship.plugin.outputs.raw_data_plugin_output import RawDataPluginOutput
from steamship.plugin.service import PluginRequest
from tests.assets.plugins.importers.plugin_file_importer import TEST_DOC, TestFileImporterPlugin

TEST_REQ = File.CreateRequest()
TEST_PLUGIN_REQ = PluginRequest(data=TEST_REQ)
TEST_PLUGIN_REQ_DICT = TEST_PLUGIN_REQ.to_dict()


def _test_resp(res):
    assert type(res) == Response
    assert type(res.data) == dict
    b64 = base64.b64encode(TEST_DOC.encode("utf-8")).decode("utf-8")
    assert res.data["data"] == b64


def test_importer():
    importer = TestFileImporterPlugin()
    res = importer.run(TEST_PLUGIN_REQ)
    _test_resp(res)

    # The endpoints take a kwargs block which is transformed into the appropriate JSON object
    res2 = importer.run_endpoint(**TEST_PLUGIN_REQ_DICT)
    _test_resp(res2)
