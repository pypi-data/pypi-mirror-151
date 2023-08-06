from typing import List, Optional

from libq.types import Command


def command_serializer(cmd: str, *, key: str, public: str = "all") -> str:
    final = f"{key}:{cmd}:{public}"
    return final


def command_deserializer(cmd: str):
    key, cmd, public = cmd.split(":")
    return Command(key=key, action=cmd, public=public)
