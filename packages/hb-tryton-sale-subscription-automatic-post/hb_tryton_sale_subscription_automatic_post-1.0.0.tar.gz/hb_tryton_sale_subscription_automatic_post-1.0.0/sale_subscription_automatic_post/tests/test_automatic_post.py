import pytest  # noqa
from datetime import date # noqa
from decimal import Decimal # noqa
from hb.tryton.devtools.helper import accounts # noqa


class TestAutomaticPost:

    def test_generated_invoice_draft(self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        self.create_chart(pool, company=company)
        with rollbacked_transaction.set_context(company=company.id):
            invoice = self.invoice_generation(pool, 'draft')
            assert invoice.state == 'draft'

    def test_generated_invoice_validated(self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        self.create_chart(pool, company=company)
        with rollbacked_transaction.set_context(company=company.id):
            invoice = self.invoice_generation(pool, 'validated')
            assert invoice.state == 'validated'

    def test_generated_invoice_posted(self, rollbacked_transaction, pool):
        company = self.get_company(pool)
        self.create_chart(pool, company=company)
        accounts.fiscal_year(company=company)
        with rollbacked_transaction.set_context(company=company.id):
            invoice = self.invoice_generation(pool, 'posted')
            assert invoice.state == 'posted'

    def get_company(self, pool):
        party = pool.get('party.party')(name="test")
        currency = pool.get('currency.currency')(
            name="euro", code='EUR', symbol='€')
        company = pool.get('company.company')(
            currency=currency, party=party)
        company.save()
        return company

    def invoice_generation(self, pool, state):
        Party = pool.get('party.party')
        Recurrence = pool.get('sale.subscription.recurrence.rule.set')
        RecurrenceRule = pool.get('sale.subscription.recurrence.rule')
        ProductTemplate = pool.get('product.template')
        Product = pool.get('product.product')
        SubscriptionService = pool.get('sale.subscription.service')
        Uom = pool.get('product.uom')
        Category = pool.get('product.category')
        Address = pool.get('party.address')

        LIST_PRICE = Decimal('500.00')

        category = Category(name="Service", accounting=True)

        product = Product()
        product_template = ProductTemplate(
            name="Service",
            type='service',
            salable=True,
            default_uom=Uom.search([('id', '=', 1)])[0],
            sale_uom=Uom.search([('id', '=', 1)])[0],
            list_price=LIST_PRICE,
            account_category=category,
            products=[product])

        ProductTemplate.save([product_template])

        rule = RecurrenceRule(freq='daily', interval=1)
        daily = Recurrence(name="Daily", rules=[rule])

        service = SubscriptionService(
            product=product_template.products[0],
            consumption_recurrence=daily)

        SubscriptionService.save([service])

        address = Address(invoice=True)
        party = Party(name="Party", addresses=[address])
        Party.save([party])

        invoice = self.generate_invoice_with_subscription(
            pool, party, service, daily, state)

        return invoice

    def generate_invoice_with_subscription(self, pool, party, service,
            recurrence, state):
        SubscriptionLine = pool.get('sale.subscription.line')
        Subscription = pool.get('sale.subscription')
        InvoiceLine = pool.get('account.invoice.line')
        CreateConsumption = pool.get(
            'sale.subscription.line.consumption.create', type='wizard')
        CreateInvoice = pool.get('sale.subscription.create_invoice',
            type='wizard')

        line = SubscriptionLine(service=service, start_date=date.today())
        line.on_change_service()

        subscription = Subscription(
                party=party,
                start_date=date.today(),
                invoice_recurrence=recurrence,
                invoice_state=state,
                lines=[line]
                )
        subscription.on_change_party()

        Subscription.save([subscription])
        Subscription.quote([subscription])
        Subscription.run([subscription])
        # import ipdb; ipdb.set_trace()

        session, start, end = CreateConsumption.create()
        create_consum = CreateConsumption(session)
        create_consum.start.date = date.today()
        create_consum._execute('create_')

        session, start, end = CreateInvoice.create()
        create_invoice = CreateInvoice(session)
        create_invoice.start.date = date.today()
        create_invoice._execute('create_')
        # import ipdb; ipdb.set_trace()

        invoice_line = InvoiceLine.search(
            [('origin', '=', subscription.lines[0])])[0]

        return invoice_line.invoice

    def get_accounts(self, pool, company=None):
        "Return accounts per kind"
        Account = pool.get('account.account')

        if not company:
            company = self.get_company(pool)

        accounts = {}
        for type in ['receivable', 'payable', 'revenue', 'expense']:
            try:
                accounts[type], = Account.search([
                        ('type.%s' % type, '=', True),
                        ('company', '=', company.id),
                        ], limit=1)
            except ValueError:
                pass
        try:
            accounts['cash'], = Account.search([
                    ('company', '=', company.id),
                    ('name', '=', 'Main Cash'),
                    ], limit=1)
        except ValueError:
            pass
        try:
            accounts['tax'], = Account.search([
                    ('company', '=', company.id),
                    ('name', '=', 'Main Tax'),
                    ], limit=1)
        except ValueError:
            pass
        return accounts

    def create_chart(
            self, pool, company=None, chart='account.account_template_root_en'):
        "Create chart of accounts"
        AccountTemplate = pool.get('account.account.template')
        ModelData = pool.get('ir.model.data')
        CreateChart = pool.get('account.create_chart', type='wizard')

        if not company:
            company = self.get_company()

        module, xml_id = chart.split('.')
        data, = ModelData.search([
                ('module', '=', module),
                ('fs_id', '=', xml_id),
                ], limit=1)

        account_template = AccountTemplate(data.db_id)

        session, start, end = CreateChart.create()
        create_chart = CreateChart(session)
        create_chart._execute('account')
        create_chart.account.account_template = account_template
        create_chart.account.company = company
        create_chart._execute('create_account')
        create_chart.properties.company = company

        accounts = self.get_accounts(pool, company=company)

        if accounts['receivable'].party_required:
            create_chart.properties.account_receivable = accounts['receivable']
        if accounts['payable'].party_required:
            create_chart.properties.account_payable = accounts['payable']
        create_chart.properties.category_account_expense = accounts['expense']
        create_chart.properties.category_account_revenue = accounts['revenue']
        create_chart._execute('create_properties')
        return create_chart
