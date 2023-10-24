from odoo import api, tools, models,fields, _
from odoo.exceptions import UserError, ValidationError
from datetime import timedelta

class PropertyOffer(models.Model):
    _name = "property.offer"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused'),
    ], string="Offer Status", default=False, copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    validity = fields.Integer("Validity", default=7)
    date_deadline= fields.Date("Date Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)
    property_id = fields.Many2one("real.estate", required=True)
    _sql_constraints = [
        ("check_offer_price_positive", "CHECK(price > 0)", "The offer price must be strictly positive")
    ]

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date and record.validity:
                create_date = record.create_date.date()
                record.date_deadline = record.create_date + timedelta(days=record.validity)
            else:
                record.date_deadline = False

    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                create_date = record.create_date.date()
                record.validity = (record.date_deadline - create_date).days

    def accepted_button(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.buyer = self.partner_id.id

    def refused_button(self):
        self.status = 'refused'
        self.property_id.buyer = False

