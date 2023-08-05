from threading import Event

from funcy import first

from testudo.runner import run, run_with_delay, OutputWindow
from testudo.task_manager import task_manager

from tests.unit.utils import tempdir


def test_simple_success():
    with tempdir() as tmp_dir:
        assert run(tmp_dir / 'test.db', 'test task', ['echo', 'hello'])
        with task_manager(tmp_dir / 'test.db') as tm:
            results = [r for r in tm.get_previous_results('test task', 2)]
            assert len(results) == 1
            assert all(r.output == 'hello' for r in results)


def test_simple_failure():
    with tempdir() as tmp_dir:
        assert not run(tmp_dir / 'test.db', 'test task', ['bash', '-c', 'printf "aA\\nbB\\ncC\\ndD\\n"; exit 42'])
        with task_manager(tmp_dir / 'test.db') as tm:
            assert first(tm.get_recent_failures('test task')).output == 'aA\nbB\ncC\ndD'


def test_custom_success_code():
    with tempdir() as tmp_dir:
        assert run(tmp_dir / 'test.db', 'test task', ['bash', '-c', 'printf "aA\\nbB\\ncC\\ndD\\n"; exit 2'], [2])
        with task_manager(tmp_dir / 'test.db') as tm:
            results = [r for r in tm.get_previous_results('test task', 2)]
            assert len(results) == 1
            assert all(r.output == 'aA\nbB\ncC\ndD' for r in results)


def test_run_with_delay():
    with tempdir() as tmp_dir:
        halt = Event()
        for count, result in enumerate(run_with_delay(tmp_dir / 'test.db', 'test task',
                                                      ['echo', 'hello'],
                                                      delay_seconds=0.2, halt_flag=halt)):
            assert result
            if count == 3:
                halt.set()
        with task_manager(tmp_dir / 'test.db') as tm:
            results = [r for r in tm.get_previous_results('test task', 5)]
            assert len(results) == 4
            assert all(r.output == 'hello' for r in results)


def test_unlimited_output_window():
    window = OutputWindow()
    for i in range(100):
        window.append(str(i))
    assert len(window.contents) == 100


def test_basic_output_window():
    window = OutputWindow()
    window.append('hello')
    assert len(window.contents) == 1
    assert window.output == 'hello'


def test_limited_output_window():
    window = OutputWindow(50)
    for i in range(100):
        window.append(str(i))
    assert len(window.contents) == 50
    assert window.contents == [str(i) for i in range(50, 100)]
    assert window.output == '\n'.join([str(i) for i in range(50, 100)])
