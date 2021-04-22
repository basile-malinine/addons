from odoo import fields, models, api
from . import hotel
from . import contract


class HotelsImport(models.TransientModel):
    _name = 'hotels.import_hz'
    _description = 'Hotels Import HZ'

    def import_test(self, param):
        print(param['hotel']['hz_id'])
        cnt = self.env['hotels.hotel'].search_count([('hz_id', '=', param['hotel']['hz_id'])])
        if cnt == 0:
            hotel_id = self.env['hotels.hotel'].create(param['hotel'])
        return cnt
