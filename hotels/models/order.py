import datetime
from dateutil import tz
from odoo import fields, models, api

ARRIVAL_TIME_LIST = [
    ('0', '00:00 - 01:00'),
    ('1', '01:00 - 02:00'),
    ('2', '02:00 - 03:00'),
    ('3', '03:00 - 04:00'),
    ('4', '04:00 - 05:00'),
    ('5', '05:00 - 06:00'),
    ('6', '06:00 - 07:00'),
    ('7', '07:00 - 08:00'),
    ('8', '08:00 - 09:00'),
    ('9', '09:00 - 10:00'),
    ('10', '10:00 - 11:00'),
    ('11', '11:00 - 12:00'),
    ('12', '12:00 - 13:00'),
    ('13', '13:00 - 14:00'),
    ('14', '14:00 - 15:00'),
    ('15', '15:00 - 16:00'),
    ('16', '16:00 - 17:00'),
    ('17', '17:00 - 18:00'),
    ('18', '18:00 - 19:00'),
    ('19', '19:00 - 20:00'),
    ('20', '20:00 - 21:00'),
    ('21', '21:00 - 22:00'),
    ('22', '22:00 - 23:00'),
    ('23', '23:00 - 00:00'),
]


class Order(models.Model):
    _name = 'hotels.order'
    _description = 'Order'

    name = fields.Char('Number', required=True)
    order_date = fields.Date('Order date')
    guest_id = fields.Many2one('res.partner', domain="[('is_guest', '=', True)]")
    arrival_date = fields.Datetime('Arrival date')
    departure_date = fields.Date('Departure date')
    arrival_time = fields.Selection(string='Arrival Time', selection=ARRIVAL_TIME_LIST, default='14')
    hotel_id = fields.Many2one('hotels.hotel', string='Hotel')
    invoice_id = fields.Many2one('hotels.invoice', string='Invoice', required=True,
                                 domain="[('hotel_id', '=', hotel_id)]")
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id)

    @api.onchange('guest_id')
    def _onchange_guest(self):
        self.guest_id.is_guest = True

    @api.onchange('hotel_id')
    def _onchange_hotel(self):
        self.invoice_id = False

    @api.onchange('invoice_id')
    def _onchange_invoice(self):
        self.update({'hotel_id': self.invoice_id.hotel_id.id})

    @api.onchange('arrival_date')
    def _onchange_arrival_date(self):
        dst_tz_name = self.env.user.tz
        if self.arrival_time:
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=int(self.arrival_time), minute=0,
                                         tzinfo=tz.gettz(dst_tz_name))
        else:
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=0, minute=0,
                                         tzinfo=tz.gettz(dst_tz_name))
        new_date = new_date.astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        self.update({'arrival_date': new_date})

    @api.onchange('arrival_time')
    def _onchange_arrival_time(self):
        if self.arrival_date:
            dst_tz_name = self.env.user.tz
            new_date = datetime.datetime(year=self.arrival_date.year, month=self.arrival_date.month,
                                         day=self.arrival_date.day, hour=int(self.arrival_time), minute=0)
            new_date = new_date.astimezone(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
            self.update({'arrival_date': new_date})
