from trytond.pool import Pool
from . import subscription
from . import configuration

__all__ = ['register']


def register():
    Pool.register(
        configuration.Configuration,
        configuration.ConfigurationService,
        subscription.SaleSubscriptionServiceType,
        subscription.SaleSubscriptionService,
        subscription.SaleSubscriptionLine,
        subscription.SaleSubscriptionLineConsumption,
        module='sale_subscription_with_variable_amount', type_='model')
    Pool.register(
        module='sale_subscription_with_variable_amount', type_='wizard')
    Pool.register(
        module='sale_subscription_with_variable_amount', type_='report')
