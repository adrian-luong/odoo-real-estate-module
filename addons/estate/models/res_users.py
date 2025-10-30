from odoo import fields, models

class EstateSalesman(models.Model):
    # _name = "estate.salesman"
    # _description = "A real estate property salesman"
    _inherit = "res.users"

    property_ids = fields.One2many('estate.property', inverse_name="salesman")
