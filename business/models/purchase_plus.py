from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class PurchasePlus(models.Model):
    _inherit = "purchase.order"
    _description = "Extend the purchase model"

    auto_generated = fields.Boolean(string='Auto Generated Purchase Order', copy=False, default=True)
    auto_sale_order_id = fields.Many2one('sale.order', string='Source Sales Order', readonly=True, copy=False)

    @api.model
    def create(self, vals):
        res = super(PurchasePlus, self).create(vals)

        sale_order_vals = {
            'partner_id': res.partner_id.id,
            'order_line': [(0, 0, {
                'product_id': line.product_id.id,
                'name': line.name,
                'product_uom': line.product_uom.id,
                'price_unit': line.price_unit,
            }) for line in res.order_line]
        }
        sale_order = self.env['sale.order'].create(sale_order_vals)

        return res
