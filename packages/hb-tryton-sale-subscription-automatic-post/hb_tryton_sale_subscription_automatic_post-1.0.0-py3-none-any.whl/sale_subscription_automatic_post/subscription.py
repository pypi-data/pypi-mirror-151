from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction
from itertools import groupby


class Subscription(metaclass=PoolMeta):
    __name__ = 'sale.subscription'

    invoice_state = fields.Selection([
        ('draft', "Draft"),
        ('validated', "Validated"),
        ('posted', "Posted")
        ], "Invoice State")

    @staticmethod
    def default_invoice_state():
        # import ipdb; ipdb.set_trace()
        pool = Pool()
        Config = pool.get('sale.configuration')

        config = Config(1)
        if config.invoice_state_default:
            return config.invoice_state_default
        else:
            return 'draft'

    @classmethod
    def generate_invoice(cls, date=None): # noqa
        pool = Pool()
        Date = pool.get('ir.date')
        Consumption = pool.get('sale.subscription.line.consumption')
        Invoice = pool.get('account.invoice')
        InvoiceLine = pool.get('account.invoice.line')

        if date is None:
            date = Date.today()

        consumptions = Consumption.search([
                ('invoice_line', '=', None),
                ('line.subscription.next_invoice_date', '<=', date),
                ('line.subscription.state', 'in', ['running', 'closed']),
                ('line.subscription.company', '=',
                    Transaction().context.get('company')),
                ],
            order=[
                ('line.subscription.id', 'DESC'),
                ])

        def keyfunc(consumption):
            return consumption.line.subscription
        invoices = {}
        lines = {}
        for subscription, consumptions in groupby(consumptions, key=keyfunc):
            invoices[subscription] = invoice = subscription._get_invoice()
            lines[subscription] = Consumption.get_invoice_lines(
                consumptions, invoice)

        all_invoices = list(invoices.values())
        Invoice.save(all_invoices)

        all_invoice_lines = []
        for subscription, invoice in invoices.items():
            invoice_lines, _ = lines[subscription]
            all_invoice_lines.extend(invoice_lines)
        InvoiceLine.save(all_invoice_lines)

        all_consumptions = []
        for values in lines.values():
            for invoice_line, consumptions in zip(*values):
                for consumption in consumptions:
                    assert not consumption.invoice_line
                    consumption.invoice_line = invoice_line
                    all_consumptions.append(consumption)
        Consumption.save(all_consumptions)

        Invoice.update_taxes(all_invoices)

        subscriptions = cls.search([
                ('next_invoice_date', '<=', date),
                ])
        for subscription in subscriptions:
            if subscription.state == 'running':
                while subscription.next_invoice_date <= date:
                    subscription.next_invoice_date = (
                        subscription.compute_next_invoice_date())
            else:
                subscription.next_invoice_date = None
        cls.save(subscriptions)

        # ------- Start of modification of the original method ------- #

        for subscription, invoice in invoices.items():
            if subscription.invoice_state in ['validated', 'posted']:
                Invoice.validate_invoice([invoice])
            if subscription.invoice_state == 'posted':
                Invoice.post([invoice])

        # -------- End of modification of the original method -------- #
