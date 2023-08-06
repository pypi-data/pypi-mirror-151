import pytest  # noqa
from hb.tryton.devtools.tests.testing import MixinTestModule


class TestModule(MixinTestModule):
    module = 'hb_bank_statement_machine_learning'
