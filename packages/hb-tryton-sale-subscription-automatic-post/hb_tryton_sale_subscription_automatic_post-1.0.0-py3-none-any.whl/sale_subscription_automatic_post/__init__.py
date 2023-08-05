from trytond.pool import Pool
from . import subscription
from . import configuration

__all__ = ['register']


def register():
    Pool.register(
        subscription.Subscription,
        configuration.Configuration,
        module='sale_subscription_automatic_post', type_='model')
    Pool.register(
        module='sale_subscription_automatic_post', type_='wizard')
    Pool.register(
        module='sale_subscription_automatic_post', type_='report')
