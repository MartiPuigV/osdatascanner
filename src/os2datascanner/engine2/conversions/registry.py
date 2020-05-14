from .utilities.results import SingleResult


__converters = {}


def conversion(input_type, *mime_types):
    """Decorator: registers the decorated function as the converter of each of
    the specified MIME types to the specified OutputType."""
    def _conversion(f):
        def _register_converter(input_type, mime_type):
            k = (input_type, mime_type)
            if k in __converters:
                raise ValueError(
                        "BUG: can't register two handlers for"
                        " the same (OutputType, MIME type) pair!", k)
            else:
                __converters[k] = f
        if mime_types:
            for m in mime_types:
                _register_converter(input_type, m)
        else:
            _register_converter(input_type, None)
        return f
    return _conversion


def convert(resource, input_type, mime_override=None) -> SingleResult:
    """Tries to convert a Resource to the specified OutputType by using the
    database of registered conversion functions.

    Raises a KeyError if no conversion exists."""
    mime_type = resource.compute_type() if not mime_override else mime_override
    try:
        converter = __converters[(input_type, mime_type)]
    except KeyError as e:
        try:
            converter = __converters[(input_type, None)]
        except KeyError:
            # Raise the original, more specific, exception
            raise e
    value = converter(resource)
    if value is not None and not isinstance(value, SingleResult):
        value = SingleResult(None, input_type, value)
    return value
