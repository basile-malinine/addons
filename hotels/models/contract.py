from odoo import fields, models, api


class Contract(models.Model):
    _name = 'hotels.contract'
    _description = 'Contract'

    name = fields.Char('Number', required=True)
    contract_date = fields.Date('Date', required=True)
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel', required=True)
    commission = fields.Integer('Commission %')
    invoices_ids = fields.One2many('hotels.invoice', 'contract_id', string='Invoices')
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.onchange('hotel_id')
    def _onchange_hotel(self):
        self.commission = self.hotel_id.commission
