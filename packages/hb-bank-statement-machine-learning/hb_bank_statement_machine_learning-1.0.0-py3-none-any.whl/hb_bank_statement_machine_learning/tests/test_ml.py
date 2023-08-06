import pytest  # noqa
from datetime import date
from random import choices
from datetime import date # noqa
from decimal import Decimal # noqa
from trytond.modules.company.tests.test_module import set_company
from hb.tryton.devtools.tests.testing import (
    get_accounts, create_chart, create_parties, get_company,
    get_statement_journal)


def create_base_statement(company, parties, journal,
                          nb_statement=10, nb_line=10):
    from trytond.pool import Pool

    pool = Pool()
    Statement = pool.get('account.statement')
    Line = pool.get('account.statement.line')
    accounts = [x for x in get_accounts(company).values()]

    statements = [
        Statement(
            name='Test %d' % x,
            date=date.today(),
            company=company,
            journal=journal,
            end_balance='100.',
            start_balance='0.',
            number_of_lines=10,
            total_amount=100,
            lines=[
                Line(
                    number='Test %d %d' % (x, y),
                    date=date.today(),
                    amount='10.',
                    account=choices(accounts)[0],
                    party=choices(parties)[0],
                )
                for y in range(nb_line)]
        )
        for x in range(nb_statement)
    ]

    Statement.save(statements)
    return [x for statement in statements for x in statement.lines]


class TestMachineLearning:

    def test_set_account_and_party_from_ml(self, rollbacked_transaction, pool):
        company = get_company()
        Line = pool.get('account.statement.line')
        with set_company(company):
            create_chart(company)
            parties = create_parties()
            journal = get_statement_journal(company)
            all_lines = create_base_statement(company, parties, journal)

            expected_line = choices(all_lines)[0]
            for _ in range(20):
                Line.copy([expected_line], dict(name=expected_line.number))

            line = Line(
                number=expected_line.number,
            )
            line.set_account_and_party_from_ml()
            assert line.account.id == expected_line.account.id

    def test_learn_error(self, rollbacked_transaction, pool):
        company = get_company()
        with set_company(company):
            create_chart(company)
            parties = create_parties()
            journal = get_statement_journal(company)
            create_base_statement(
                company, parties, journal, nb_statement=1, nb_line=1)

    def test_predict_error(self, rollbacked_transaction, pool):
        company = get_company()
        with set_company(company):
            create_chart(company)
            Line = pool.get('account.statement.line')
            line = Line(number='test')
            line.set_account_and_party_from_ml()

    def test_write(self, rollbacked_transaction, pool):
        company = get_company()
        with set_company(company):
            create_chart(company)
            parties = create_parties()
            journal = get_statement_journal(company)
            all_lines = create_base_statement(company, parties, journal)
            expected_line = choices(all_lines)[0]
            expected_line.amount = '20.'
            expected_line.save()

    def test_delete(self, rollbacked_transaction, pool):
        company = get_company()
        with set_company(company):
            create_chart(company)
            parties = create_parties()
            journal = get_statement_journal(company)
            all_lines = create_base_statement(company, parties, journal)
            expected_line = choices(all_lines)[0]
            Line = pool.get('account.statement.line')
            Line.delete([expected_line])

    def test_on_change(self, rollbacked_transaction, pool):
        company = get_company()
        with set_company(company):
            create_chart(company)
            Line = pool.get('account.statement.line')
            line = Line()
            line.on_change_number()
