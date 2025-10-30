from odoo import fields, models, api, exceptions

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags of a real estate property"
    _order = "name"

    name = fields.Char('Name', required=True)
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name), ('id', '!=', record.id)]) > 0:
                raise exceptions.ValidationError('The property tag name must be unique!')

    property_ids = fields.One2many("estate.property", inverse_name="id")

    color = fields.Integer('Color')