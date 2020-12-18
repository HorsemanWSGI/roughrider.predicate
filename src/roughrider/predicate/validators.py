from abc import ABC, abstractmethod
from typing import Iterable, Tuple, Optional, Callable, Any, Union
from roughrider.predicate.errors import Error, ConstraintsErrors


class Validator(ABC):
    """A validator.
    """
    description: Optional[str]

    @abstractmethod
    def __call__(self, *args, **namespace) -> None:
        """Raises a roughrider.predicate.Error if the validation failed.
        """


Constraint = Union[Validator, Callable[..., None]]


class Or(Tuple[Constraint], Validator):

    def __call__(self, *args, **namespace):
        errors = []
        for validator in self:
            try:
                validator(*args, **namespace)
                return
            except Error as exc:
                errors.append(exc)
            except ConstraintsErrors as exc:
                errors.extend(exc.errors)

        raise ConstraintsErrors(*errors)


def resolve_validators(validators: Iterable[Constraint],
                       *args, **namespace) -> Optional[ConstraintsErrors]:
    errors = []
    for validator in validators:
        try:
            validator(*args, **namespace)
        except Error as exc:
            errors.append(exc)
        except ConstraintsErrors as exc:
            errors.extends(exc.errors)
    if errors:
        return ConstraintsErrors(*errors)
