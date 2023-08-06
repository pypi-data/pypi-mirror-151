from __future__ import annotations

from typing import Any, Dict

from pydantic import BaseModel

from steamship.base.configuration import Configuration


def event_to_config(event: dict) -> Configuration:
    if event is None:
        raise Exception("Null event provided")
    if "invocationContext" not in event:
        raise Exception("invocationContext not in event")

    return Configuration.from_dict(event["invocationContext"])


class Verb:
    GET = "GET"
    POST = "POST"

    @staticmethod
    def safely_from_str(s: str) -> str:
        # TODO (enias): Is this needed?
        ss = s.strip().upper()
        if ss == Verb.GET:
            return Verb.GET
        elif ss == Verb.POST:
            return Verb.POST
        return s


class Invocation(BaseModel):
    httpVerb: str = None
    appPath: str = None  # e.g. /hello/there
    arguments: Dict[str, Any] = None
    config: Dict[str, Any] = None

    @staticmethod
    def from_dict(d: dict) -> Invocation:
        return Invocation(
            httpVerb=d.get("httpVerb"),
            appPath=d.get("appPath"),
            arguments=d.get("arguments"),
            config=d.get("config"),
        )


class Request(BaseModel):
    """An request of a method on an app instance.

    This is the payload sent from the public-facing App Proxy to the
    private-facing app microservice.
    """

    # TODO (enias): Is this a replacement for the Request in base?

    clientConfig: Configuration = None
    invocation: Invocation = None

    @staticmethod
    def from_dict(d: dict) -> Request:
        invocation = Invocation.from_dict(d.get("invocation", dict()))
        client_config = Configuration.from_dict(
            d.get("clientConfig", dict())
        )  # TODO (enias): Review config dict
        return Request(clientConfig=client_config, invocation=invocation)
