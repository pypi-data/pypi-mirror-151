from legion_utils import Priority
from yaml import safe_load

from testudo.config import TaskConfig
from testudo.reporter import report
from testudo.task_manager import task_manager

from tests.unit.utils import tempdir

BASIC_CONFIG = TaskConfig(**safe_load('''
task_id: testing task
delay_seconds: 1
command: echo hello
legion:
  exchange: test
  route: stuff
  reporting_delay_seconds: 0.5
  failure_priority_thresholds:
    - num_failures: 2
      priority: WARNING
    - num_failures: 4
      priority: ERROR
    - num_failures: 6
      priority: CRITICAL'''))


def test_report_missing_task():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('test', 'test output 1', 0, None)
            msg = report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert msg.priority == Priority.ERROR


def test_basic_report():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 0, None)
            msg = report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert msg.priority == Priority.INFO
            assert msg.contents['recent_output'] == 'test output 1'


def test_report_single_failure():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            msg = report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert msg.priority == Priority.INFO
            assert msg.contents['recent_output'] == 'test output 1'


def test_report_warning_failures():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            tm.insert_task_result('testing task', 'test output 2', 1, None)
            msg = report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert msg.priority == Priority.WARNING
            assert msg.contents['recent_output'] == 'test output 2'


def test_report_error_failures():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            tm.insert_task_result('testing task', 'test output 2', 1, None)
            tm.insert_task_result('testing task', 'test output 3', 1, None)
            tm.insert_task_result('testing task', 'test output 4', 1, None)
            msg = report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert msg.priority == Priority.ERROR
            assert msg.contents['recent_output'] == 'test output 4'


def test_report_critical_failures():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            tm.insert_task_result('testing task', 'test output 1', 1, None)
            tm.insert_task_result('testing task', 'test output 2', 1, None)
            tm.insert_task_result('testing task', 'test output 3', 1, None)
            tm.insert_task_result('testing task', 'test output 4', 1, None)
            tm.insert_task_result('testing task', 'test output 5', 1, None)
            tm.insert_task_result('testing task', 'test output 6', 1, None)
            tm.insert_task_result('testing task', 'test output 7', 1, None)
            msg = report(tmp_dir / 'test.db', BASIC_CONFIG)
            assert msg.priority == Priority.CRITICAL
            assert msg.contents['recent_output'] == 'test output 7'
