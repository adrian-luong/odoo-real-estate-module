from datetime import datetime, timedelta
from odoo import api, fields, models, exceptions
from odoo.tools.float_utils import float_is_zero, float_compare

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for a real estate property"
    _order = "price desc"

    # region Offer price field
    price = fields.Float('Price')
    _positive_price = models.Constraint(
        "CHECK(price >= 0)", "The offer price must be strictly positive"
    )

    # endregion

    # region Offer status field
    status = fields.Selection(
        [('accepted', 'Accepted'), ('refused', 'Refused')],
        string='Status', copy=False
    )
    @api.constrains('status')
    def _check_status(self):
        for  record in self:
            if record.status == 'accepted' and self.search_count([('status', '=', 'accepted')]) > 1:
                raise exceptions.ValidationError('There can only be one accepted offer for each property')

    # endregion

    # region Validity - Deadline fields
    validity = fields.Integer('Validity (days)', default=7)
    deadline = fields.Date('Deadline', compute="_compute_deadline", inverse="_inverse_validity")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            # FIX: Prevent re-computation if the field has been set by the inverse
            if 'deadline' in record._cache:
                continue

            if isinstance(record.create_date, datetime):
                record.deadline = record.create_date.date() + timedelta(days=record.validity)
            else:
                record.deadline = fields.Date.today() + timedelta(days=record.validity)

    @api.onchange('deadline')
    def _inverse_validity(self):
        for record in self:
            if isinstance(record.create_date, datetime):
                record.validity = (record.deadline - record.create_date.date()).days
            else:
                record.validity = (record.deadline - fields.Date.today()).days

    # endregion

    # region Many2One fields
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)
    property_type_id = fields.Many2one('estate.property.type', related="property_id.type_id", store=True)

    # endregion

    # region Action buttons
    def accept_offer(self):
        for record in self:
            has_expected_price = not float_is_zero(record.property_id.expected_price, precision_digits=2)
            less_than_90_percent = float_compare(record.price, record.property_id.expected_price * 0.9, precision_digits=2) == -1

            if has_expected_price and less_than_90_percent:
                raise exceptions.ValidationError("The offering price must be at least 90 percent of the property's expected price.")
            else:
                record.status = 'accepted'
                record.property_id.buyer = record.partner_id
                record.property_id.selling_price = record.price

        return True

    def refuse_offer(self):
        for record in self:
            record.status = 'refused'

        return True

    # endregion

    # region CRUD
    @api.model
    def create(self, vals):
        record = self.env['estate.property'].browse(vals['property_id'])
        record.state = 'offer_received'
        return super().create(vals)

    # endregion