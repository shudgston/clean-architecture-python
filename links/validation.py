from urllib.parse import urlparse
from _collections import defaultdict


def is_url(url):
    parsed = urlparse(url)
    if parsed.scheme and parsed.netloc:
        if parsed.scheme in ['http', 'https']:
            return True
    return False


def validate(request, schema):
    """

    :param request:
    :param schema:
    :return:
    """
    assert isinstance(request, dict), "request must be a dictionary"
    assert isinstance(schema, dict), "schema must be a dictionary"
    errors = defaultdict(list)

    for key, rule in schema.items():
        assert isinstance(rule, Schema), "rule must be instance of Schema"
        testval = request.get(key)

        if rule.required and testval is None or not testval:
            errors[key].append('Value is required')
            break

        if rule.maxlength and len(testval) > rule.maxlength:
            errors[key].append('Value exceeds maximum length {}'.format(
                rule.maxlength))

        for custom in rule.custom:
            f, help = custom
            if not f(testval):
                    errors[key].append(help)

    return (len(errors) == 0, errors,)


class Schema:

    def __init__(self, required=False, maxlength=0, custom=None):
        """

        :param required:
        :param maxlength:
        :param custom:
        """
        self.required = required
        self.maxlength = maxlength

        if custom is None:
            custom = []
        self.custom = custom
