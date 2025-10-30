from odoo import fields, models, api, exceptions

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "The type of a real estate property"
    _order = "name"

    name = fields.Char('Name', required=True)
    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if self.search_count([('name', '=', record.name), ('id', '!=', record.id)]) > 0:
                raise exceptions.ValidationError('The property type name must be unique!')

    property_ids = fields.One2many("estate.property", inverse_name="id")

    # region Offer fields
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_type_id", string="Offers")
    offer_count = fields.Integer(default=0, compute="_compute_offer_count", store=True)

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    # endregion
