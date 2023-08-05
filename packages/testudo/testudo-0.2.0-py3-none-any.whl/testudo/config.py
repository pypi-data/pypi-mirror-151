from typing import List,  Optional

from legion_utils import Priority, priority_of
from pydantic import validator
from pydantic.dataclasses import dataclass


class Strict:
    extra = "forbid"


@dataclass(config=Strict)
class FailurePriorityThreshold:
    num_failures: int
    priority: Priority

    @validator('priority', pre=True, allow_reuse=True)
    def _priority(cls, v: str) -> Priority:  # pylint: disable=E0213,R0201
        return priority_of(v)


@dataclass(config=Strict)
class LegionConfig:
    exchange: str
    route: str
    failure_priority_thresholds: List[FailurePriorityThreshold]
    reporting_delay_seconds: float


@dataclass(config=Strict)
class TaskConfig():
    task_id: str
    delay_seconds: float
    command: str
    legion: LegionConfig
    acceptable_return_codes: Optional[List[int]] = None
    initial_delay_seconds: Optional[float] = None
    on_failure_delay_seconds: Optional[float] = None
