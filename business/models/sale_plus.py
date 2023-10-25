from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class SaleOrder(models.Model):
    """Inherit to create PO while create SO"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Super the function to create PO to the corresponding company
           when confirming the SO"""
        res = super(SaleOrder, self).action_confirm()
        company_id = self.env['res.company'].search(
            [('name', '=', self.partner_id.name)])
        transit_locations = self.env['stock.location'].search(
            [('active', '=', True), ('usage', '=', 'transit')])
        self.env['purchase.order'].create({
            'partner_id': self.env.company.id,
            'company_id': company_id.id,
            'origin': self.name,
            'order_line': [(0, 0, {
                'product_id': record.product_id.id,
                'product_qty': record.product_uom_qty,
                'price_unit': record.price_unit,
                'price_subtotal': record.price_subtotal,
            }) for record in self.order_line],
        })
        return res