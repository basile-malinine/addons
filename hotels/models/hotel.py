from odoo import fields, models, api

NUM_STARS_LIST = [('a', 'None'), ('b', '1'), ('c', '2'), ('d', '3'), ('e', '4'), ('f', '5')]

FINE_PERIOD_LIST = [
    ('hours_14', '14:00 on the day of arrival'),
    ('hours_18', '18:00 on the day of arrival'),
    ('days_2',   'Until 2 days before arrival'),
    ('days_3',   'Until 3 days before arrival'),
    ('days_5',   'Until 5 days before arrival'),
    ('days_7',   'Until 7 days before arrival'),
]

FINE_SIZE_LIST = [
    ('first_night', 'The cost of the first night'),
    ('percent_50',  '50% of the total price'),
    ('percent_100', '100% of the total price'),
]


class Hotel(models.Model):
    _name = 'hotels.hotel'
    _description = 'Hotel'

    name = fields.Char('Name', required=True)
    num_stars = fields.Selection(string='Stars', selection=NUM_STARS_LIST, default='a')
    city_id = fields.Many2one('hotels.city', string='City')
    address = fields.Char('Address')
    phone = fields.Char('Phone')
    email = fields.Char('E-Mail')
    hotelier_id = fields.Many2one('res.partner', string='Hotelier', domain="[('is_hotelier', '=', True)]")
    fine_period = fields.Selection(selection=FINE_PERIOD_LIST)
    fine_size = fields.Selection(selection=FINE_SIZE_LIST)
    banks_ids = fields.One2many('res.partner.bank', 'hotel_id', string='Bank Accounts')
    contacts_ids = fields.Many2many('res.partner', string='Contacts')
    contracts_ids = fields.One2many('hotels.contract', 'hotel_id', string='Contracts')
    commission = fields.Integer('Commission %', default=12)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)
    invoices_ids = fields.One2many('hotels.invoice', 'hotel_id', string='Invoices')

    @api.onchange('hotelier_id')
    def _onchange_hotelier(self):
        self.hotelier_id.is_hotelier = True

    def import_test(self, msg):
        print(msg['a'])

