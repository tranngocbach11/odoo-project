from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class PurchasePlus(models.Model):
    _inherit = "purchase.order"
    _description = "Extend the purchase model"

    auto_generated = fields.Boolean(string='Auto Generated Purchase Order', copy=False)
    auto_sale_order_id = fields.Many2one('sale.order', string='Source Sales Order', readonly=True, copy=False)

