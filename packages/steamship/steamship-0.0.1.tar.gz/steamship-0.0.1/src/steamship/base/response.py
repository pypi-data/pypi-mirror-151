from __future__ import annotations

import time
from typing import Generic, Type, TypeVar

from pydantic.generics import GenericModel

from steamship.base.tasks import *

T = TypeVar("T")  # Declare type variable


class Response(GenericModel, Generic[T]):
    expect: Type[T] = None
    task: Task = None
    data: T = None
    error: SteamshipError = None
    client: Any = None

    class Config:
        arbitrary_types_allowed = True  # This is required to support SteamshipError

    def update(self, response: Response[T]):
        if self.task is not None and response.task is not None:
            self.task.refresh(response.task)
        if response.data is not None:
            self.data = response.data
        self.error = response.error

    def wait(self, max_timeout_s: float = 60, retry_delay_s: float = 1):
        """Polls and blocks until the task has succeeded or failed (or timeout reached)."""
        start = time.time()
        if self.task is None or self.task.state == TaskState.failed:
            return

        self.check()
        if self.task is not None:
            if self.task.state == TaskState.succeeded or self.task.state == TaskState.failed:
                return
        else:
            return
        time.sleep(retry_delay_s)

        while time.time() - start < max_timeout_s:
            time.sleep(retry_delay_s)
            self.check()
            if self.task is not None:
                if self.task.state == TaskState.succeeded or self.task.state == TaskState.failed:
                    return
            else:
                return

    def check(self):
        if self.task is None:
            return
        req = TaskStatusRequest(taskId=self.task.task_id)
        resp = self.client.post("task/status", payload=req, expect=self.expect)
        self.update(resp)

    def add_comment(
        self,
        external_id: str = None,
        external_type: str = None,
        external_group: str = None,
        metadata: Any = None,
    ) -> IResponse[TaskComment]:
        if self.task is not None:
            return self.task.add_comment(
                external_id=external_id,
                external_type=external_type,
                external_group=external_group,
                metadata=metadata,
            )

    def list_comments(self) -> IResponse[TaskCommentList]:
        if self.task is not None:
            return self.task.list_comments()

    def delete_comment(self, comment: TaskComment = None) -> IResponse[TaskComment]:
        if self.task is not None:
            return self.task.delete_comment(comment=comment)
