from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.model import fields
from trytond.cache import Cache
from .bank_ml import BankML


class Line(metaclass=PoolMeta):
    __name__ = 'account.statement.line'

    _get_machine_learning_cache = Cache(__name__ + '.get_machine_learning')

    @classmethod
    def get_machine_learning(cls):
        """Method cached with the time LRU to return the machine learning"""
        transaction = Transaction()
        company = transaction.context['company']
        ml = cls._get_machine_learning_cache.get(company)
        if not ml:
            ml = BankML()
            try:
                ml.learn()
            except ValueError:
                pass  # no enough data

            cls._get_machine_learning_cache.set(company, ml)

        return ml

    def set_account_and_party_from_ml(self):
        """Fill the party and account from the machine learning prediction"""
        if not self.number:
            return

        pool = Pool()
        cls = pool.get(self.__name__)
        ml = cls.get_machine_learning()
        account, party = ml.predict(self.number)
        if account:
            self.account = pool.get('account.account')(account)

        if party:
            self.party = pool.get('party.party')(party)

    @fields.depends('number')
    def on_change_number(self):
        self.set_account_and_party_from_ml()

    @classmethod
    def create(cls, vlist):
        cls._get_machine_learning_cache.clear()
        return super().create(vlist)

    @classmethod
    def write(cls, *args):
        super().write(*args)
        cls._get_machine_learning_cache.clear()

    @classmethod
    def delete(cls, *args):
        cls._get_machine_learning_cache.clear()
        super().delete(*args)
