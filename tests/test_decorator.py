import pytest
from roughrider.predicate.errors import ConstraintError, ConstraintsErrors
from roughrider.predicate.decorator import with_predicates


def validate_document(doc):
    errors = []
    if not doc:
        errors.append(ConstraintError('Document is empty'))
    if not getattr(doc, 'id', None):
        errors.append(ConstraintError('Document does not have an id'))
    if errors:
        raise ConstraintsErrors(*errors)


def test_simple_decorator():

    @with_predicates([validate_document])
    def handle_doc(doc):
        pass

    with pytest.raises(ConstraintsErrors) as err:
        handle_doc(None)

    assert err.value.json() == '''[{"message": "Document is empty"}, {"message": "Document does not have an id"}]'''
