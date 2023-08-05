from math import ceil
from pathlib import Path
from pprint import pformat
from socket import gethostname
from threading import Thread, Event
from traceback import format_exc
from typing import Optional

from funcy import first
import legion_utils
from legion_utils import Priority, NotificationMsg

from testudo.config import TaskConfig
from testudo.log import log
from testudo.task_manager import task_manager

HOSTNAME = gethostname()


def report(db: Path, task_config: TaskConfig) -> NotificationMsg:
    with task_manager(db) as tm:
        if recent_failures := list(f for f in tm.get_recent_failures(task_config.task_id)):
            priority_thresholds = sorted(task_config.legion.failure_priority_thresholds,
                                         key=lambda t: t.num_failures, reverse=True)
            for threshold in priority_thresholds:
                if len(recent_failures) >= threshold.num_failures:
                    return NotificationMsg(contents={'src': HOSTNAME,
                                                     'recent_output': recent_failures[0].output,
                                                     'recent_exit_code': recent_failures[0].exit_code},
                                           alert_key=f'[{HOSTNAME}][testudo][failure][{task_config.task_id}]',
                                           desc=f'Task [{task_config.task_id}] failed {len(recent_failures)} times',
                                           ttl=ceil(task_config.legion.reporting_delay_seconds * 2),
                                           priority=threshold.priority)
        if most_recent_run := first(tm.get_previous_results(task_config.task_id, limit=1)):
            return NotificationMsg(contents={'src': HOSTNAME,
                                             'recent_output': most_recent_run.output},
                                   desc=f'Task [{task_config.task_id} ran nominally',
                                   priority=Priority.INFO)
        return NotificationMsg(contents={'src': HOSTNAME},
                               alert_key=f'[{HOSTNAME}][testudo][unknown_task_id][{task_config.task_id}]',
                               desc=f'No runs detected for {task_config.task_id}',
                               ttl=ceil(task_config.legion.reporting_delay_seconds * 2),
                               priority=Priority.ERROR)


def publish_report(db: Path, task_config: TaskConfig) -> Optional[NotificationMsg]:
    rpt = report(db, task_config)
    try:
        legion_utils.broadcast_msg(task_config.legion.exchange, task_config.legion.route, rpt)
        return rpt
    except (AssertionError, SyntaxError):
        raise  # pragma: no cover # exists only for passing through errors in testing
    except Exception:  # pylint: disable=W0703
        log.error(f'Unable to report on task execution\nStack Trace:\n{format_exc()}')
        log.error(f'UNPUBLISHED REPORT:\n{pformat(rpt)}')
    return None


def run_reporter(db: Path, task_config: TaskConfig, halt: Event) -> None:
    while 42:
        publish_report(db, task_config)
        if halt.wait(task_config.legion.reporting_delay_seconds):
            return None


def start_reporter_daemon(db: Path, task_config: TaskConfig, halt: Optional[Event] = None) -> Thread:
    reporter_thread = Thread(target=run_reporter,
                             args=(db, task_config, halt),
                             daemon=True)
    reporter_thread.start()
    return reporter_thread
