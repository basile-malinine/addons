from odoo import fields, models, api
from . import hotel
from . import contract


class HotelsImport(models.TransientModel):
    _name = 'hotels.import_hz'
    _description = 'Hotels Import HZ'

    def import_test(self, param):
        record_ids = self.env['hotels.contract'].search([('id', '!=', 0)])
        names = []
        for record in record_ids:
            names.append(record.name)
        return names
