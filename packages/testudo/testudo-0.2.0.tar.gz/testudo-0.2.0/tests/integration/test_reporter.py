from threading import Event
from time import sleep

from pytest_mock import MockerFixture
from yaml import safe_load

from testudo.config import TaskConfig
from testudo.reporter import publish_report, start_reporter_daemon
from testudo.task_manager import task_manager

from tests.unit.utils import tempdir

EXCHANGE = 'test_exchange'
ROUTE = 'test.route'
BASIC_CONFIG = TaskConfig(**safe_load(f'''
task_id: testing task
delay_seconds: 1
command: echo hello
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


def test_report_publishing(mocker: MockerFixture):
    def mock_broadcast_msg(exchange, route, msg):
        assert exchange == EXCHANGE
        assert route == ROUTE
        assert msg.contents['recent_output'] == "test output 2"

    mocker.patch('legion_utils.broadcast_msg', mock_broadcast_msg)
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            tm.insert_task_result('testing task', 'test output 2', 1, None)
            report = publish_report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert report is not None


def test_report_publishing_failure(mocker: MockerFixture):
    def mock_broadcast_msg(exchange, route, msg):
        assert exchange == EXCHANGE
        assert route == ROUTE
        assert msg.contents['recent_output'] == "test output 2"
        raise RuntimeError("Shit happens")

    mocker.patch('legion_utils.broadcast_msg', mock_broadcast_msg)
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            tm.insert_task_result('testing task', 'test output 2', 1, None)
            report = publish_report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert report is None


def test_report_publishing_loop(mocker: MockerFixture):
    def mock_broadcast_msg(exchange, route, msg):
        assert exchange == EXCHANGE
        assert route == ROUTE
        assert msg.contents['recent_output'].startswith("test output")

    mocker.patch('legion_utils.broadcast_msg', mock_broadcast_msg)
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            tm.insert_task_result('testing task', 'test output 2', 1, None)
            halt_flag = Event()
            daemon = start_reporter_daemon(tmp_dir / 'test.db', BASIC_CONFIG, halt=halt_flag)
            sleep(2)
            halt_flag.set()
            previous_runs = [r for r in tm.get_previous_results('testing task', 2)]
            daemon.join()
            assert len(previous_runs) >= 1
