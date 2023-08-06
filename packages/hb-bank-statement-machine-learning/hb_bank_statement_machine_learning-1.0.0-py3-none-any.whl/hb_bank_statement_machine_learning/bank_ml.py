from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from trytond.pool import Pool


class BankML(object):

    def __init__(self):
        self.pipeline_account = None
        self.pipeline_party = None

    def learn(self):
        """Use the existing account.statement.line to fill the machine
        learning

        :param pool: instance of the **Pool** of the tryton's model
        :param from_date: date since the line is learned
        """
        pool = Pool()
        data = []
        target_account = []
        target_party = []

        StmtLine = pool.get('account.statement.line')

        offset = 0
        limit = 80
        while True:
            objs = StmtLine.search([], offset=offset, limit=limit)
            for o in objs:
                data.append(o.number)
                target_account.append(o.account.id if o.account else "")
                target_party.append(o.party.id if o.party else "")

            offset += limit
            if len(objs) < limit:
                break

        self.pipeline_account = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf-svm', SGDClassifier(
                loss='hinge', penalty='l2', alpha=1e-3, random_state=42
            )),
        ])
        self.pipeline_account.fit(data, target_account)

        self.pipeline_party = Pipeline([
            ('vect', CountVectorizer()),
            ('tfidf', TfidfTransformer()),
            ('clf-svm', SGDClassifier(
                loss='hinge', penalty='l2', alpha=1e-3, random_state=42
            )),
        ])
        self.pipeline_party.fit(data, target_party)

    def predict(self, bank_stmt_label):
        """Return the party and the account predicted by the given label

        :param bank_stmt_label: the given label
        return: account id, party id
        """
        if not self.pipeline_party or not self.pipeline_account:
            return None, None

        predicted_party = self.pipeline_party.predict([bank_stmt_label])
        predicted_account = self.pipeline_account.predict([bank_stmt_label])
        return predicted_account[0], predicted_party[0]
