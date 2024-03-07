from trytond.pool import Pool
from . import invoices
from . import party
from . import renter

def register():
    Pool.register(
        invoices.RentalInvoices,
        invoices.RentalInvoicesElectricity,
        party.Party,
        renter.RentalRenter,
        module='rental_invoices', type_='model')
