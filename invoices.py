from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import Pool
from trytond.pyson import Eval
import datetime


class RentalInvoices(ModelSQL, ModelView):
    """Rental Invoices"""
    __name__ = 'rental.invoices.rental'

    year = fields.Date('Year', required=True,
                       context={'date_format': '%Y'})
    month = fields.Many2One('ir.calendar.month', "Month", required=True)
    rental_month = fields.Numeric('Rental per month',
                                  digits=(16, Eval('currency_digits', 2)),
                                  depends=['currency_digits'])
    total_rental_month = fields.Function(fields.Numeric('Total rental per month', readonly=True,
                                                        digits=(16, Eval('currency_digits', 2)),
                                                        depends=['currency_digits']),
                                         'get_total_rental_month')
    currency = fields.Many2One('currency.currency',
                               'Currency', readonly=True)
    currency_digits = fields.Function(fields.Integer('Currency Digits'),
                                      'on_change_with_currency_digits')
    dividor = fields.Integer('Dividor')
    electricity_invoice = fields.Many2One('rental.invoices.electricity', 'Electricity invoice')
    invoice_internet_total = fields.Numeric('Invoice internet',
                                            digits=(16, Eval('currency_digits', 2)), depends=['currency_digits'])
    result_invoice_internet = fields.Function(
        fields.Numeric('Result invoice internet', readonly=True,
                       digits=(16, Eval('currency_digits', 2)), depends=['currency_digits']),
        'get_result_invoice_internet')
    comments = fields.Text('Comments')
    renters = fields.One2Many('rental.invoices.renter',
                              'rental', 'Renters')

    @classmethod
    def default_year(cls):
        return str(datetime.date.today().year)

    @classmethod
    def default_currency(cls):
        Currency = Pool().get('currency.currency')
        currency = Currency.search(
            [('code', '=', 'EUR')], limit=1)
        return currency[0].id if currency else None

    def get_total_rental_month(self, name=None):
        if self.renters:
            total_rental = sum(r.total_pay_renter for r in self.renters
                               if r.total_pay_renter)
            return self.currency.round(total_rental) if self.currency else total_rental
        return 0

    def get_result_invoice_internet(self, name=None):
        if self.invoice_internet_total and self.dividor and self.currency:
            result = self.invoice_internet_total / self.dividor
            return self.currency.round(result)
        return 0

    @fields.depends('currency')
    def on_change_with_currency_digits(self, name=None):
        if self.currency:
            return self.currency.digits
        return 2


class RentalInvoicesElectricity(ModelSQL, ModelView):
    """Rental Invoices Electricity"""
    __name__ = 'rental.invoices.electricity'
    _rec_name = 'code'

    code = fields.Char('Invoice code')
    year = fields.Date('Year', required=True,
                       context={'date_format': '%Y'})
    month = fields.Many2One('ir.calendar.month', "Month", required=True)
    invoice_total = fields.Numeric('Invoice total',
                                   digits=(16, Eval('currency_digits', 2)),
                                   depends=['currency_digits'])
    currency = fields.Many2One('currency.currency', 'Currency', readonly=True)
    currency_digits = fields.Function(fields.Integer('Currency Digits'),
                                      'on_change_with_currency_digits')
    dividor = fields.Integer('Dividor', required=True)
    result_dividor = fields.Function(
        fields.Numeric('Dividor result', digits=(16, Eval('currency_digits', 2)),
                       depends=['currency_digits']), 'get_result_dividor')
    comment = fields.Text('Comment')

    @classmethod
    def default_currency(cls):
        Currency = Pool().get('currency.currency')
        currency = Currency.search(
            [('code', '=', 'EUR')], limit=1)
        return currency[0].id if currency else None

    @classmethod
    def default_year(cls):
        return str(datetime.date.today().year)

    def get_result_dividor(self, name=None):
        if self.invoice_total and self.dividor and self.currency:
            result = self.invoice_total / self.dividor
            return self.currency.round(result)
        return 0

    def get_rec_name(self, name=None):
        if self.month and self.invoice_total and self.currency:
            return self.month.name + ' - ' + \
                str(self.currency.round(self.invoice_total)) + self.currency.symbol
        else:
            return self.code

    @fields.depends('currency')
    def on_change_with_currency_digits(self, name=None):
        if self.currency:
            return self.currency.digits
        return 2
