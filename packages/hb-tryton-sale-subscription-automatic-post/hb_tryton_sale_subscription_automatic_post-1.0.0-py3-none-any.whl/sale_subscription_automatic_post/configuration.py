from trytond.model import fields
from trytond.pool import PoolMeta


class Configuration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'

    invoice_state_default = fields.Selection([
        ('draft', "Draft"),
        ('validated', "Validated"),
        ('posted', "Posted")
        ], "Default Subscription invoice state")
