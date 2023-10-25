from odoo import api, models, tools, fields, _
from odoo.exceptions import UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"
    _description = "Extend the purchase model"

    def button_confirm(self):
        """Override the button confirm function to create a SO
        for the corresponding company when confirming the PO."""
        res = super(PurchaseOrder, self).button_confirm()
        company_id = self.env['res.company'].search(
            [('name', '=', self.partner_id.name)], limit=1)
        if company_id:
            sale_order_vals = {
                'partner_id': self.partner_id.id,
                'company_id': company_id.id,
                'client_order_ref': self.name,
                'order_line': [(0, 0, {
                    'product_id': rec.product_id.id,
                    'product_uom_qty': rec.product_qty,
                    'price_unit': rec.price_unit,
                    'tax_id': [(6, 0, rec.taxes_id.ids)],  # Chuyển đổi danh sách các ID sang kiểu tuple (6, 0, [ids])
                    'price_subtotal': rec.price_subtotal
                }) for rec in self.order_line]
            }
            self.env['sale.order'].sudo().create(sale_order_vals)
        return res

