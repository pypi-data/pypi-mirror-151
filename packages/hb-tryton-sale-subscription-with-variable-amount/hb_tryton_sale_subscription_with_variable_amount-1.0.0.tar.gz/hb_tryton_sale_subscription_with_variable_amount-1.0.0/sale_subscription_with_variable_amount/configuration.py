from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.pyson import Eval
from trytond.modules.sale.configuration import default_func
from trytond.model import ModelSQL
from trytond.modules.company.model import CompanyValueMixin


class Configuration(metaclass=PoolMeta):
    'Product Configuration'
    __name__ = 'product.configuration'

    service_type = fields.MultiValue(fields.Many2One(
        'sale.subscription.service.type', "Service type",
        required=True,
        domain=[
            ('company', 'in',
             [Eval('context', {}).get('company', -1), None]),
        ]))

    default_service_type = default_func('service_type')

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'service_type':
            return pool.get('product.configuration.service')

        return super(Configuration, cls).multivalue_model(field)


class ConfigurationService(ModelSQL, CompanyValueMixin):
    "product Configuration Service"
    __name__ = 'product.configuration.service'
    service_type = fields.Many2One(
        'sale.subscription.service.type', "Service type",
        required=True,
        domain=[
            ('company', 'in',
             [Eval('context', {}).get('company', -1), None]),
        ],
        depends=['company'])

    @classmethod
    def default_service_type(cls):
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        return ModelData.get_id(
            'sale_subscription_with_variable_amount',
            'default_service_type')
