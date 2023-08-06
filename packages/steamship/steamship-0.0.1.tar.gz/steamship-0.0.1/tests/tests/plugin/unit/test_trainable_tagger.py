from assets.plugins.taggers.plugin_trainable_tagger import (
    TRAIN_RESPONSE,
    TRAINING_PARAMETERS,
    TestTrainableTaggerPlugin,
)

from steamship import File
from steamship.app.response import Response
from steamship.data.block import Block
from steamship.plugin.inputs.block_and_tag_plugin_input import BlockAndTagPluginInput
from steamship.plugin.inputs.train_plugin_input import TrainPluginInput
from steamship.plugin.inputs.training_parameter_plugin_input import TrainingParameterPluginInput
from steamship.plugin.outputs.block_and_tag_plugin_output import BlockAndTagPluginOutput
from steamship.plugin.service import PluginRequest
from tests.utils.client import get_steamship_client

TEST_REQ = BlockAndTagPluginInput(
    file=File(
        blocks=[
            Block(
                id="ABC",
                text="Once upon a time there was a magical ship. "
                "The ship was powered by STEAM. The ship went to the moon.",
            )
        ]
    )
)
TEST_PLUGIN_REQ = PluginRequest(data=TEST_REQ, plugin_instance_id="000")
TEST_PLUGIN_REQ_DICT = TEST_PLUGIN_REQ.to_dict()


def _test_resp(res):
    pass
    # assert len(res.data.file.tags) == 3
    # TODO: Finish writing tests in a future PR once the general design of this is finished.


def test_trainable_tagger():
    client = get_steamship_client()
    assert client is not None

    plugin = TestTrainableTaggerPlugin(client=client)
    assert plugin.client is not None

    # STEP 1. Training Parameters
    # The first part of trainable is to produce trainable parameters. The end-user may offer inputs to this,
    # but ultimately it is the plugin itself which decides upon the final set of trainable parameters.
    tagger1 = plugin.get_training_parameters(
        PluginRequest(data=TrainingParameterPluginInput(), task_id="000", plugin_instance_id="000")
    )
    assert tagger1.data == TRAINING_PARAMETERS.to_dict()
    tagger2 = plugin.get_training_parameters_endpoint(
        **PluginRequest(
            data=TrainingParameterPluginInput(), task_id="000", plugin_instance_id="000"
        ).to_dict()
    )
    assert tagger2.data == TRAINING_PARAMETERS.to_dict()
    assert tagger2.data["trainingEpochs"] == TRAINING_PARAMETERS.training_epochs

    # STEP 2. Training
    # The first part of trainable is to produce your own trainable parameters.
    tagger1 = plugin.train(
        PluginRequest(
            data=TrainPluginInput(
                plugin_instance="foo", training_params=TRAINING_PARAMETERS.training_params
            ),
            task_id="000",
            plugin_instance_id="000",
        )
    )
    assert tagger1.data == TRAIN_RESPONSE.to_dict()

    tagger2 = plugin.train_endpoint(
        **PluginRequest(
            data=TrainPluginInput(
                plugin_instance="foo", training_params=TRAINING_PARAMETERS.training_params
            ),
            task_id="000",
            plugin_instance_id="000",
        ).to_dict()
    )
    assert tagger2.data == TRAIN_RESPONSE.to_dict()

    # STEP 3. Run
    res = plugin.run(TEST_PLUGIN_REQ)
    _test_resp(res)

    # The endpoints take a kwargs block which is transformed into the appropriate JSON object
    res2 = plugin.run_endpoint(**TEST_PLUGIN_REQ_DICT)
    _test_resp(res2)
