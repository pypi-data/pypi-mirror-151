import pytest  # noqa
from datetime import date # noqa


class TestDefaultInvoiceState:

    def test_default_invoice_state_empty(self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        with rollbacked_transaction.set_context(company=company.id):
            invoice_state = self.get_subscription_invoice_state(pool)

            assert invoice_state == 'draft'

    def test_default_invoice_state_draft(self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        with rollbacked_transaction.set_context(company=company.id):
            invoice_state = self.get_subscription_invoice_state(
                pool, state='draft')

            assert invoice_state == 'draft'

    def test_default_invoice_state_validated(
            self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        with rollbacked_transaction.set_context(company=company.id):
            invoice_state = self.get_subscription_invoice_state(
                pool, state='validated')

            assert invoice_state == 'validated'

    def test_default_invoice_state_posted(self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        with rollbacked_transaction.set_context(company=company.id):
            invoice_state = self.get_subscription_invoice_state(
                pool, state='posted')

            assert invoice_state == 'posted'

    def get_company(self, pool):
        party = pool.get('party.party')(name="test")
        currency = pool.get('currency.currency')(
            name="euro", code='EUR', symbol='€')
        company = pool.get('company.company')(
            currency=currency, party=party)
        company.save()
        return company

    def get_subscription_invoice_state(self, pool, state=None):
        Subscription = pool.get('sale.subscription')
        Party = pool.get('party.party')
        Recurrence = pool.get('sale.subscription.recurrence.rule.set')
        RecurrenceRule = pool.get('sale.subscription.recurrence.rule')
        Configuration = pool.get('sale.configuration')

        if state:
            config = Configuration(invoice_state_default=state)
            Configuration.save([config])

        party = Party(name="Party")
        rule = RecurrenceRule(freq='daily', interval=1)
        daily = Recurrence(name="Daily", rules=[rule])
        subscription = Subscription(
            party=party,
            start_date=date.today(),
            invoice_recurrence=daily)
        Subscription.save([subscription])

        return subscription.invoice_state
