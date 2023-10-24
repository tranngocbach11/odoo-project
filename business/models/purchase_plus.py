from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class PurchasePlus(models.Model):
    _inherit = "purchase.order"
    _description = "Extend the purchase model"

    purchase_name = fields.Char("Purchase Name")