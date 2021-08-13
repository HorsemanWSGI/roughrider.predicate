from functools import wraps
import typing as t
from roughrider.predicate.errors import ConstraintError, ConstraintsErrors


Error = t.Union[HTTPConstraintError, ConstraintError, ConstraintsErrors]
Predicates = t.Iterable[t.Callable[[...], t.Any]]
PredicateErrorHandler = t.Callable[[Error], t.Any]


def with_predicates(
        predicates: Predicates, handler: PredicateErrorHandler = None):
    def predication_wrapper(func):
        @wraps(func)
        def assert_predicates(*args, **kwargs):
            for predicate in predicates:
                try:
                    predicate(*args, **kwargs)
                except (ConstraintError, ConstraintsErrors) as exc:
                    if handler is not None:
                        return handler(exc)
                    raise
            return func(*args, **kwargs)
        return assert_predicates
    return predication_wrapper
