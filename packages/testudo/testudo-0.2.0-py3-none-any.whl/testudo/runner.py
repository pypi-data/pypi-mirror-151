from functools import partial
from pathlib import Path
from shlex import split
from subprocess import STDOUT, Popen, PIPE  # nosec
from threading import Event
from typing import List, Optional, Generator, Union, Set

from testudo.config import TaskConfig
from testudo.log import log
from testudo.reporter import start_reporter_daemon
from testudo.task_manager import task_manager


def report_failure(db: Path, task_id: str, output: str, exit_code: int, stack_trace: Optional[str] = None) -> None:
    with task_manager(db) as tm:
        tm.report_failure(task_id, output, exit_code, stack_trace)


def report_success(db: Path, task_id: str, output: str) -> None:
    with task_manager(db) as tm:
        tm.report_success(task_id, output)


class OutputWindow:
    def __init__(self, limit: Optional[int] = None) -> None:
        self.limit = limit
        self.contents: List[str] = []

    def append(self, line: str) -> None:
        self.contents.append(line)
        if self.limit is not None:
            while len(self.contents) > self.limit:
                self.contents.pop(0)

    @property
    def output(self) -> str:
        joined = '\n'.join(self.contents)
        return joined


def run(db: Path, task_id: str, cmd: List[str],
        success_codes: Optional[Union[List[int], Set[int]]] = None) -> bool:
    log.info(f"Running Task [{task_id}]...")
    success_codes = success_codes or {0}
    out = OutputWindow(30)
    # this is the whole point of the program, to run arbitrary commands
    with Popen(cmd, stderr=STDOUT, stdout=PIPE, shell=False) as proc:  # nosec
        while proc.poll() is None:
            line = []
            if proc.stdout is None:  # pragma: no branch
                break  # pragma: no cover
            for byte in iter(partial(proc.stdout.read, 1), b''):
                char = byte.decode()
                if char not in {'\n', '\r', ''}:
                    line.append(char)
                else:
                    joined = "".join(line)
                    log.info(f'[{task_id}] OUTPUT: {joined}')
                    out.append(joined.rstrip())
                    line = []
        exit_code = proc.returncode
        if exit_code in success_codes:
            log.info(f"Task [{task_id}] successful!")
            report_success(db, task_id, out.output)
            return True
        log.warning(f"Task [{task_id}] failed!")
        report_failure(db, task_id, out.output, exit_code)
        return False


def run_with_delay(db: Path, task_id: str,
                   cmd: List[str],
                   delay_seconds: float,
                   halt_flag: Event,
                   initial_delay_seconds: Optional[float] = None,
                   on_failure_delay_seconds: Optional[float] = None,
                   success_codes: Optional[List[int]] = None) -> Generator[bool, None, None]:
    on_failure_delay_seconds = on_failure_delay_seconds or delay_seconds
    halt_flag.wait(timeout=initial_delay_seconds or 0.0)
    while 42:
        success = run(db, task_id, cmd, success_codes)
        yield success
        if halt_flag.wait(delay_seconds if success else on_failure_delay_seconds):
            break


def run_with_reporter(db: Path, config: TaskConfig, halt: Optional[Event] = None) -> None:
    first_run_complete = False
    _halt = halt or Event()
    for _ in run_with_delay(db, config.task_id, split(config.command),
                            delay_seconds=config.delay_seconds, halt_flag=_halt,
                            initial_delay_seconds=config.initial_delay_seconds,
                            on_failure_delay_seconds=config.on_failure_delay_seconds,
                            success_codes=config.acceptable_return_codes):
        if not first_run_complete:
            first_run_complete = True
            start_reporter_daemon(db, config, halt=_halt)
