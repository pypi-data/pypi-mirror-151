from contextlib import contextmanager
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Generator

from testudo.task_manager import TaskManager, task_manager
from tests.unit.utils import tempdir


def test_task_manager_basic_task_result_insert():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        tm.insert_task_result('test', 'test output', 0, None)
        tm.close()


def test_task_manager_basic_task_result_insert_multiple_close():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        tm.insert_task_result('test', 'test output', 0, None)
        tm.close()
        tm.close()


def test_task_manager_basic_task_result_insert_multiple_setup():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        tm._setup()
        tm.insert_task_result('test', 'test output', 0, None)
        tm.close()
        tm.close()


def test_task_manager_basic_task_result_get():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        result_id = tm.insert_task_result('test', 'test output', 0, None)
        result = tm.get_task_result(result_id)
        assert result.task_id == 'test'
        assert result.output == 'test output'
        tm.close()

def test_basic_previous_results_get():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        result_ids = [tm.insert_task_result('test', 'test output 1', 0, None),
                      tm.insert_task_result('test', 'test output 2', 0, None),
                      tm.insert_task_result('test', 'test output 3', 0, None),
                      tm.insert_task_result('test', 'test output 4', 0, None)]
        previous_runs = tm.get_previous_results('test', 2)
        assert [p.result_id for p in previous_runs] == [str(i) for i in result_ids[-2:][::-1]]

def test_recent_failures():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        result_ids = [tm.insert_task_result('test', 'test output 1', 1, None),
                      tm.insert_task_result('test', 'test output 2', 0, None),
                      tm.insert_task_result('test', 'test output 3', 1, None),
                      tm.insert_task_result('test', 'test output 4', 1, None)]
        recent_failures = tm.get_recent_failures('test')
        assert [p.result_id for p in recent_failures] == [str(i) for i in result_ids[-2:][::-1]]

def test_no_recent_failures():
    with tempdir() as tmp_dir:
        tm = TaskManager(tmp_dir / 'test.db')
        result_ids = [tm.insert_task_result('test', 'test output 1', 1, None),
                      tm.insert_task_result('test', 'test output 2', 0, None),
                      tm.insert_task_result('test', 'test output 3', 1, None),
                      tm.insert_task_result('test', 'test output 4', 1, None)]
        assert not any(tm.get_recent_failures('not-test'))

def test_task_manager_context():
    with tempdir() as tmp_dir:
        with task_manager(tmp_dir / 'test.db') as tm:
            result_id = tm.insert_task_result('test', 'test output', 0, None)
            result = tm.get_task_result(result_id)
            assert result.task_id == 'test'
            assert result.output == 'test output'
