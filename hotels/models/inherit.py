from odoo import fields, models


class Partner(models.Model):
    _inherit = 'res.partner'
    is_guest = fields.Boolean()
    is_hotelier = fields.Boolean()


class ResPartnerBank(models.Model):
    _inherit = 'res.partner.bank'
    hotel_id = fields.Many2one('hotels.hotel', 'Hotel', ondelete='cascade', index=True)
