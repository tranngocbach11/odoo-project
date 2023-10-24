from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class SalePlus(models.Model):
    _inherit = "sale.order"
    _description = "Extend the sale model"

    sale_name = fields.Char("Sale Name")