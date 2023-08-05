from collections import namedtuple
from contextlib import contextmanager
from itertools import takewhile
from pathlib import Path
from sqlite3 import Connection, connect
from time import time
from typing import Union, Optional, Generator
from uuid import UUID, uuid4 as uuid

from funcy import first


TaskResult = namedtuple('TaskResult', ('result_id', 'task_id', 'timestamp',
                        'output', 'exit_code', 'stack_trace'))


class TaskManager:
    ALL_TABLES = """SELECT name FROM sqlite_schema
                    WHERE type IN ('table','view')
                    AND name NOT LIKE 'sqlite_%'
                    ORDER BY 1;"""
    TASK_RESULTS_EXISTS = """SELECT name
                             FROM sqlite_master
                             WHERE type='table' AND name='task_results'"""
    CREATE_TASK_RESULTS = """CREATE TABLE task_results(
                             result_id CHARACTER(37) NOT NULL PRIMARY KEY,
                             task_id TEXT NOT NULL,
                             timestamp NUMERIC NOT NULL,
                             output TEXT NOT NULL,
                             exit_code INTEGER NOT NULL,
                             stack_trace TEXT)"""
    INSERT_TASK_RESULT = """INSERT INTO task_results VALUES (?, ?, ?, ?, ?, ?)"""
    GET_TASK_RESULT = """SELECT * FROM task_results WHERE result_id = ?"""
    GET_PREVIOUS_RESULTS = """SELECT * FROM task_results
                              WHERE task_id = ?
                              ORDER BY timestamp DESC
                              LIMIT ?"""
    GET_RESULTS_SORTED = """SELECT *
                            FROM task_results
                            WHERE task_id = ?
                            ORDER BY timestamp DESC"""

    def __init__(self, db: Path):
        self.db = str(db)
        self.connection: Optional[Connection] = None
        self._setup()

    @property
    def _connection(self) -> Connection:
        if self.connection is None:
            self.connection = connect(self.db)
        return self.connection

    def close(self) -> None:
        if self.connection is not None:
            self.connection.close()
            self.connection = None

    def _task_results_table_exists(self) -> bool:
        with self._connection as con:
            return any(row for row in con.execute(TaskManager.TASK_RESULTS_EXISTS))

    def _create_task_results_table(self) -> None:
        with self._connection as con:
            con.execute(TaskManager.CREATE_TASK_RESULTS)

    def _insert_task_result(self, result_id: Union[str, UUID],
                            task_id: str, timestamp: float,
                            output: str, exit_code: int,
                            stack_trace: Optional[str] = None) -> None:
        with self._connection as con:
            con.execute(TaskManager.INSERT_TASK_RESULT, (str(result_id), task_id,
                                                         timestamp, output,
                                                         exit_code, stack_trace))

    def insert_task_result(self, task_id: str, output: str, exit_code: int,
                           stack_trace: Optional[str] = None) -> Union[str, UUID]:
        timestamp = time()
        result_id = uuid()
        self._insert_task_result(result_id, task_id, timestamp,
                                 output, exit_code, stack_trace)
        return result_id

    def get_task_result(self, result_id: Union[str, UUID]) -> TaskResult:
        with self._connection as con:
            return TaskResult(*first(  # pragma: no branch
                row for row in con.execute(
                    TaskManager.GET_TASK_RESULT,
                    (str(result_id),))))

    def get_previous_results(self, task_id: str,
                             limit: int) -> Generator[TaskResult, None, None]:
        with self._connection as con:
            return (TaskResult(*row) for row in con.execute(
                TaskManager.GET_PREVIOUS_RESULTS, (task_id, limit)))

    def get_recent_failures(self, task_id: str) -> Generator[TaskResult, None, None]:
        with self._connection as con:
            cursor = con.cursor()
            cursor.execute(TaskManager.GET_RESULTS_SORTED, (task_id,))
            for result in takewhile(lambda r: r.exit_code != 0, (TaskResult(*row) for row in cursor)):
                yield result
            cursor.close()

    def _setup(self) -> None:
        if not self._task_results_table_exists():
            self._create_task_results_table()

    def report_success(self, task_id: str, result_output: str) -> str:
        return str(self.insert_task_result(task_id, result_output, 0))

    def report_failure(self, task_id: str, result_output: str,
                       exit_code: int, stack_trace: Optional[str] = None) -> str:
        return str(self.insert_task_result(task_id, result_output,
                                           exit_code, (stack_trace or '')))


@contextmanager
def task_manager(db: Path) -> Generator[TaskManager, None, None]:
    tm = TaskManager(db)
    try:
        yield tm
    finally:
        tm.close()
