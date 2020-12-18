import json
from dataclasses import dataclass
from typing import List, NamedTuple, Iterable


@dataclass(frozen=True)
class Error(Exception):
    message: str


class ConstraintsErrors(Exception):
    errors: List[Error]

    def __init__(self, *errors: Error):
        self.errors = list(errors)

    def __iter__(self):
        return iter(self.errors)

    def __len__(self):
        return len(self.errors)

    def __eq__(self, other):
        if isinstance(other, ConstraintsErrors):
            return self.errors == other.errors
        elif isinstance(other, Iterable):
            return self.errors == other
        return False

    def json(self):
        return json.dumps([e.__dict__ for e in self.errors])
