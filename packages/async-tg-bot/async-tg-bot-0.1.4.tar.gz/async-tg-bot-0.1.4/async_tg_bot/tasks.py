from dataclasses import dataclass, field
from typing import Any


@dataclass
class Task:
    func: Any
    delay: int = 0


@dataclass
class Tasks:
    _tasks: list[Task] = field(default_factory=list)

    def add(self, task: Task):
        self._tasks.append(task)

    def run(self):
        for task in self._tasks:
            task.func()
