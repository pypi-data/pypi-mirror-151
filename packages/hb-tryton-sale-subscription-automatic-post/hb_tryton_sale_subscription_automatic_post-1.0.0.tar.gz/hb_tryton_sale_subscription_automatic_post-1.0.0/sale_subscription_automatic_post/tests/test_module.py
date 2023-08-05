import pytest  # noqa
from hb.tryton.devtools.tests.testing import MixinTestModule


class TestModule(MixinTestModule):
    module = 'sale_subscription_automatic_post'
