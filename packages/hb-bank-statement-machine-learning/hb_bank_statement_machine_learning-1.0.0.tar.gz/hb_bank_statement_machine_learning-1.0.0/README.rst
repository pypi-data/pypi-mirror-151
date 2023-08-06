#########################################
Hb Bank Statement Machine Learning Module
#########################################

This module add a machine learning on the **account.bank.statement** to predict
the party and the account to use for a new line.

*******
Install
*******

Dependencies for ArchLinux

.. code-block::

    sudo pacman -S cairo pkgconf gobject-introspection


Dependencies for debian


.. code-block::

    sudo apt-get install libcairo2-dev libgirepository1.0-dev


Install the package

.. code-block::

    # installs python deps
    pip install hb_bank_statement_machine_learning
    # install the module
    trytond-admin -u hb_bank_statement_machine_learning --activate-dependencies


Install the db by hb-tryton-devtools

.. code-block::

    pip install git+https://gitlab.com/hashbangfr/tryton-modules/hb_tryton_devtools.git#egg=hb_tryton_devtools
    export TRYTON_DATABASE_URI=postgresql:///
    export TRYTON_DATABASE_NAME=test
    hb-tryton-admin create-db --modules hb_bank_statement_machine_learning


************
Test package
************

The package need pytest and hb-tryton-devtools

.. code-block::

    pip install pytest pytest-cov
    pip install git+ssh://git@gitlab.com/hashbangfr/tryton-modules/hb_tryton_devtools.git#egg=hb_tryton_devtools


Run the test with pytest with environ variable

.. code-block::

    export TRYTON_DATABASE_URI=postgresql:///
    export TRYTON_DATABASE_NAME=test
    pytest hb_bank_statement_machine_learning/tests


*********
Low level
*********

The machine learning is added on the **acount.statement.line**, the machine learning is based on the field number on the line,
this field must be filled

.. code-block::

    pool = Pool()
    Line = pool.get('account.statement.line')
    line = Line()
    line.number = 'My number'
    line.set_account_and_party_from_ml()
    assert line.party
    assert line.account

*****
Usage
*****

An on_change method on the field number exist to predict the fields party and account from the interface

*********
CHANGELOG
*********

1.0.0 (2022-05-18)
------------------

* Used cache from trytond

0.1.0 (2021-09-28)
------------------

* Implemented the machine learning
* Implemented the on change method on the fields number
