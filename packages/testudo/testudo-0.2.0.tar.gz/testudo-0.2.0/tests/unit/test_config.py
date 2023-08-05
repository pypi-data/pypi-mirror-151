from typing import Any

from yaml import safe_load
from pytest import mark, raises

from testudo.config import TaskConfig

TESTDATA = [
    ('''
task_id: testing task
delay_seconds: 1
initial_delay_seconds: 0.1
command: echo hello
acceptable_return_codes: [0, 1]
legion:
  exchange: test
  route: stuff
  reporting_delay_seconds: 0.5
  failure_priority_thresholds:
    - num_failures: 1
      priority: WARNING
    - num_failures: 3
      priority: ERROR
    - num_failures: 5
      priority: CRITICAL
''', None),
]


@mark.parametrize("config,exc", TESTDATA)
def test_config_loading(config: Any, exc: BaseException) -> None:
    if exc is not None:
        with raises(exc):
            config = TaskConfig(**safe_load(config))
    else:
        config = TaskConfig(**safe_load(config))
