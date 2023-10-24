from odoo import api, tools, models, fields, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from datetime import datetime, timedelta

class Estate(models.Model):
    _name = "real.estate"
    _description = "The real estate model"
    _order = "id desc"

    def _default_availability_date(self):
        today = datetime.today()
        return today + timedelta(days=90)

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Post Code")
    date_availability = fields.Date("Date Availability", copy=False, default=_default_availability_date)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], "Garden Orientation")
    active = fields.Boolean("Active", default=True)
    status = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('cancel', 'Cancel')
    ], "Status", default="new")
    property_type = fields.Many2one("estate.property", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    salesperson = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    tags = fields.Many2many("property.tag", string="Tag", widget="colorpicker")
    offers = fields.One2many("property.offer", "property_id", string="Offers")
    total_area = fields.Integer("Total Area", compute="_compute_total")
    best_price = fields.Float(string="Best Price", compute="_compute_best_price")
    _sql_constraints = [
        ("check_expected_price_positive", "CHECK(expected_price > 0)", "The expected price must be strictly positive"),

    ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offers.price")
    def _compute_best_price(self):
        for record in self:
            if record.offers:
                record.best_price = max(record.offers.mapped('price'))
            else:
                record.best_price = 0.0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area=10
            self.garden_orientation="north"
        else:
            self.garden_area=0
            self.garden_orientation=False

    def sold_button(self):
        for record in self:
            if record.status == "cancel":
                raise UserError("Cancel property cannot be sold.")
            record.status = "sold"

    def cancel_button(self):
        for record in self:
            if record.status == "sold":
                raise UserError("Sold property cannot be canceled.")
            record.status = "cancel"

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not float_is_zero(record.expected_price, precision_digits=2) and not float_is_zero(record.selling_price, precision_digits=2):
                if float_compare(record.selling_price, 0.9 * record.expected_price, precision_digits=2) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price!")



