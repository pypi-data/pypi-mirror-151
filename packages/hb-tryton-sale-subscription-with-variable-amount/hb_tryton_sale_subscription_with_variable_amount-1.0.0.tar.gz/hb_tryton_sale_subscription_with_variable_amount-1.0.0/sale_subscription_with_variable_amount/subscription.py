from itertools import groupby
from trytond.transaction import Transaction
from trytond.tools import sortable_values
from trytond.i18n import gettext
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta, Pool
from trytond.modules.sale_subscription.exceptions import InvoiceError
from trytond.modules.company.model import CompanyValueMixin


class SaleSubscriptionServiceType(ModelSQL, ModelView, CompanyValueMixin):
    "Type of the subscription's service"
    __name__ = 'sale.subscription.service.type'

    # TODO add company
    # TODO place in configuration to defined the default value

    name = fields.Char("Name of the type of service")

    consumption_hook = fields.Selection(
        [
            ('fixed', 'The quantity is defined on the subscription line'),
        ],
        "Hook to create the consumption line",
        required=True,
        help="Defined the hook to use for get the quantity")

    invoice_hook = fields.Selection(
        [
            (
                'fixed',
                (
                    'The quantity and price unit are defined on the '
                    'subscription line'
                )
            ),
        ],
        "Hook to create the invoice line",
        required=True,
        help="Defined the hook to use for get the quantity or price unit")

    @staticmethod
    def default_company():
        return Transaction().context.get('company')

    @staticmethod
    def default_consumption_hook():
        return 'fixed'

    @staticmethod
    def default_invoice_hook():
        return 'fixed'

    def apply_consumption_hook(self, line):
        method = f'consumption_hook_{self.consumption_hook}'
        getattr(self, method)(line)

    def apply_invoice_hook(self, line, sub_consumptions):
        method = f'invoice_hook_{self.invoice_hook}'
        getattr(self, method)(line, sub_consumptions)

    def consumption_hook_fixed(self, line):
        pass

    def invoice_hook_fixed(self, line, sub_consumptions):
        pass


class SaleSubscriptionService(metaclass=PoolMeta):
    __name__ = 'sale.subscription.service'

    service_type = fields.Many2One(
        'sale.subscription.service.type',
        "Service type",
        required=True)

    @classmethod
    def default_service_type(cls, **pattern):
        Config = Pool().get('product.configuration')
        config = Config(1)
        return config.get_multivalue('service_type', **pattern).id


class SaleSubscriptionLine(metaclass=PoolMeta):
    __name__ = 'sale.subscription.line'

    def get_consumption(self, date):
        consumption = super().get_consumption(date)
        if consumption is None:
            return

        self.service.service_type.apply_consumption_hook(consumption)
        return consumption


class SaleSubscriptionLineConsumption(metaclass=PoolMeta):
    __name__ = 'sale.subscription.line.consumption'

    @classmethod
    def get_invoice_lines(cls, consumptions, invoice):
        "Return a list of lines and a list of consumptions"
        pool = Pool()
        InvoiceLine = pool.get('account.invoice.line')

        lines, grouped_consumptions = [], []
        consumptions = sorted(
            consumptions, key=sortable_values(cls._group_invoice_key))
        for key, sub_consumptions in groupby(
                consumptions, key=cls._group_invoice_key):
            sub_consumptions = list(sub_consumptions)
            values = dict(key)
            service_type = values.pop('service_type')

            line = InvoiceLine(**values)
            line.invoice = invoice
            line.on_change_invoice()
            line.type = 'line'
            line.quantity = sum(c.quantity for c in sub_consumptions)

            line.on_change_product()
            service_type.apply_invoice_hook(line, sub_consumptions)

            if not line.account:
                raise InvoiceError(
                    gettext(
                        'sale_subscription'
                        '.msg_consumption_invoice_missing_account_revenue',
                        product=line.product.rec_name))

            lines.append(line)
            grouped_consumptions.append(sub_consumptions)
        return lines, grouped_consumptions

    @classmethod
    def _group_invoice_key(cls, consumption):
        return (
            ('company', consumption.line.subscription.company),
            ('currency', consumption.line.subscription.currency),
            ('unit', consumption.line.unit),
            ('product', consumption.line.service.product),
            ('unit_price', consumption.line.unit_price),
            ('description', consumption.line.description),
            ('origin', consumption.line),
            ('service_type', consumption.line.service.service_type),
        )
