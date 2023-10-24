from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class PropertyTag(models.Model):
    _name = "property.tag"
    _order = "name"

    name = fields.Char("Tag", required=True)
    color = fields.Integer(string="Color")
    _sql_constraints = [
        ("unique_tag_name", "UNIQUE(name)", "The tag name must be unique")
    ]