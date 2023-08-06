from trytond.pool import Pool

__all__ = ['register']


def register():
    from . import account  # cause cache

    Pool.register(
        account.Line,
        module='hb_bank_statement_machine_learning', type_='model')
    Pool.register(
        module='hb_bank_statement_machine_learning', type_='wizard')
    Pool.register(
        module='hb_bank_statement_machine_learning', type_='report')
