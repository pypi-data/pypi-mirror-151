from pprint import pformat
from threading import Event, Thread
from time import sleep

from pytest_mock import MockerFixture
from yaml import safe_load

from testudo.config import TaskConfig
from testudo.runner import run_with_reporter
from testudo.task_manager import task_manager

from tests.unit.utils import tempdir

EXCHANGE = 'test_exchange'
ROUTE = 'test.route'
BASIC_CONFIG = TaskConfig(**safe_load(f'''
task_id: testing task
delay_seconds: 1
command: 'printf "hello\\nhow\\nare\\nyou\\n"'
legion:
  exchange: {EXCHANGE}
  route: {ROUTE}
  reporting_delay_seconds: 0.5
  failure_priority_thresholds:
    - num_failures: 2
      priority: WARNING
    - num_failures: 4
      priority: ERROR
    - num_failures: 6
      priority: CRITICAL'''))


def test_running_and_report_publishing_loop(mocker: MockerFixture):
    def mock_broadcast_msg(exchange, route, msg):
        assert exchange == EXCHANGE
        assert route == ROUTE
        print(pformat(msg.contents))
        assert msg.contents['recent_output'] == "hello\nhow\nare\nyou"

    mocker.patch('legion_utils.broadcast_msg', mock_broadcast_msg)
    with tempdir() as tmp_dir:
        halt_flag = Event()
        thread = Thread(target=run_with_reporter, args=(tmp_dir / 'test.db', BASIC_CONFIG, halt_flag))
        thread.start()
        sleep(2)
        halt_flag.set()
        thread.join(timeout=5.0)
        assert not thread.is_alive()
        with task_manager(tmp_dir / 'test.db') as tm:
            previous_runs = [r for r in tm.get_previous_results('testing task', 2)]
            assert len(previous_runs) >= 1
