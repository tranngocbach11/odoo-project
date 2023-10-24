from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Property of Estate"
    _order = "name"

    name = fields.Char("Estate Property Type", required=True)
    property_ids = fields.One2many("real.estate", "property_type")
    sequence = fields.Integer(string='Sequence')
    _sql_constraints = [
        ("unique_property_type", "UNIQUE(name)", "The property type name must be unique")
    ]