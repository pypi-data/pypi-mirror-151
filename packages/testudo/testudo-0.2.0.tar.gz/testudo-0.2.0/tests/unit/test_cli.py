from typing import Any

from pytest import mark
from click.testing import CliRunner

from testudo.cli import main


# TESTDATA = [
#     ('{"user_name": "Eugene", "hello_suffix": "?"}', "Hello, Eugene?\n", 0),
# ]


# @mark.parametrize("config,exp_output,exp_code", TESTDATA)
# def test_cli_basics(config: Any, exp_output: Any, exp_code: Any):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         with open('config.yaml', 'w') as config_file:
#             config_file.write(config)
#         result = runner.invoke(main, ['-c', 'config.yaml'])
#         assert result.exit_code == exp_code
#         assert exp_output in result.output


# @mark.parametrize("config,exp_output,exp_code", TESTDATA)
# def test_cli_debug(config: Any, exp_output: Any, exp_code: Any):
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         with open('config.yaml', 'w') as config_file:
#             config_file.write(config)
#         result = runner.invoke(main, ['-c', 'config.yaml', '--debug'])
#         assert result.exit_code == exp_code
#         assert exp_output in result.output
