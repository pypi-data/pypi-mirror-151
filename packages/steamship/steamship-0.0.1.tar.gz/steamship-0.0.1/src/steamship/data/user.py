from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from steamship.app import Response
from steamship.base import Client


class User(BaseModel):
    client: Client = None
    id: str = None
    handle: str = None

    @staticmethod
    def from_dict(d: Any, client: Client = None) -> User:
        if d["user"] is not None:
            d = d["user"]

        return User(
            client=client,
            id=d.get("id"),
            handle=d.get("handle"),
        )

    def to_dict(self) -> dict:
        return dict(id=self.id, handle=self.handle)

    @staticmethod
    def current(client: Client) -> Response[User]:
        return client.get("account/current", expect=User)
