from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import Eval
from decimal import Decimal


class RentalRenter(ModelSQL, ModelView):
    """Rental Invoices Renter"""
    __name__ = 'rental.invoices.renter'

    renter = fields.Many2One('party.party', "Renter")
    rental = fields.Many2One('rental.invoices.rental', "Rental Invoice")
    quantity_rental = fields.Numeric("Quantity rental", digits=(16, 2))
    currency_digits = fields.Function(fields.Integer('Currency Digits'),
                                      'on_change_with_currency_digits')
    payment_electricity = fields.Function(
        fields.Numeric("Payment electricity", digits=(16, Eval('currency_digits', 2)),
                       depends=['currency_digits']), 'get_payment_electricity')
    total_pay_renter = fields.Function(
        fields.Numeric("Total amount payable per renter", digits=(16, Eval('currency_digits', 2)),
                       depends=['currency_digits']), 'get_total_pay_renter')
    not_payment_electricity = fields.Boolean("Not payment electricity",
                                             help=(
                                                 "If this case is mark, the renter not colaborate in the invoice "
                                                 "electricity"))

    @fields.depends('_parent_rental.currency')
    def on_change_with_currency_digits(self, name=None):
        if self.rental and self.rental.currency:
            return self.rental.currency.digits
        return 2

    def get_payment_electricity(self, name=None):
        if self.not_payment_electricity:
            return 0
        if (self.rental is not None and self.rental.currency
                and self.rental.electricity_invoice is not None):
            result_dividor = self.rental.electricity_invoice.result_dividor
            if result_dividor is not None:
                return self.rental.currency.round(result_dividor)
        return 0

    def get_total_pay_renter(self, name=None):
        total_payment = 0
        if self.quantity_rental:
            total_payment += self.quantity_rental
        if self.payment_electricity:
            total_payment += self.payment_electricity
        return total_payment
