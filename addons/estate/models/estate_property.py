from datetime import timedelta
from odoo import fields, models, api, exceptions
from odoo.tools.float_utils import float_compare, float_is_zero

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Details of a real estate property"
    _order = "sequence, id desc"

    # region Foreign Keys
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    tag_ids = fields.Many2many("estate.property.tag", string="Property Tags")
    offer_ids = fields.One2many("estate.property.offer", inverse_name="property_id", string="Offers")
    salesman = fields.Many2one("res.users", string="Salesman")
    buyer = fields.Many2one("res.partner", string="Buyer")

    # endregion

    # region Text/String/Char fields
    name = fields.Char('Name', required=True, default="Unknown")
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')

    # endregion

    # region Date/Datetime fields
    date_availability = fields.Date(
        'Available Date', copy=False,
        default=fields.Date.today() + timedelta(days=90)
    )
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)

    # endregion

    # region Float fields
    expected_price = fields.Float('Expected Price', required=True)
    _positive_expected_price = models.Constraint(
        "CHECK(expected_price >= 0)", "The expected price must be strictly positive"
    )

    selling_price = fields.Float('Selling Price', readonly=True, copy=False)
    _positive_selling_price = models.Constraint(
        "CHECK(selling_price >= 0)", "The selling price must be strictly positive"
    )

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price_on_expected_price(self):
        """
        Ensures the selling price is at least 90% of the property's expected price.
        """
        for record in self:
            has_expected_price = not float_is_zero(record.expected_price, precision_digits=2)
            has_selling_price = not float_is_zero(record.selling_price, precision_digits=2)
            less_than_90_percent = float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1

            if has_expected_price and has_selling_price and less_than_90_percent:
                raise exceptions.ValidationError("The selling price must be at least 90 percent of the property's expected price.")

    best_offer = fields.Float('Best Offer', compute="_compute_best_price")
    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            offer_prices = [offer.price for offer in record.offer_ids]
            record.best_offer = max(offer_prices) if len(offer_prices) > 0 else record.expected_price

    # endregion

    # region Integer fields
    sequence = fields.Integer('Sequence', default=1)
    bedrooms = fields.Integer('Bedrooms', default=2)
    living_area = fields.Integer('Living Area (sqm)')
    facades = fields.Integer('Facades')
    garden_area = fields.Integer('Garden Area (sqm)')

    total_area = fields.Integer('Total Area (sqm)', compute="_compute_total_area")
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    # endregion

    # region Boolean fields
    garage = fields.Boolean('Garage')
    active = fields.Boolean(default=False)

    garden = fields.Boolean('Garden')
    @api.onchange('garden')
    def _on_has_garden(self):
        self.garden_area = 10
        self.garden_orientation = 'north'

    # endregion

    # region Selection/Enum fields
    garden_orientation = fields.Selection(
        [('east', 'East'), ('west', 'West'), ('south', 'South'), ('north', 'North')],
        string='Garden Orientation',
    )
    state = fields.Selection(
        [
            ('new', 'New'), ('sold', 'Sold'), ('cancelled', 'Cancelled'),
            ('offer_received', 'Offer Received'),
            ('offer_accepted', 'Offer Accepted')
        ],
        string='State', required=True, copy=False, default='new'
    )

    # endregion

    # region Action buttons
    def sell_property(self):
        for record in self:
            if record.state != 'cancelled':
                record.state = 'sold'
            else:
                raise exceptions.UserError('Cancelled property cannot be sold')

        return True

    def cancel_property(self):
        for record in self:
            if record.state != 'sold':
                record.state = 'cancelled'
            else:
                raise exceptions.UserError('Sold property cannot be cancelled')

        return True

    # endregion

    # region CRUD
    @api.ondelete(at_uninstall=False)
    def _handle_delete(self):
        for record in self:
            if any(record.state not in ['new', 'cancelled']):
                raise exceptions.ValidationError("Can't delete an active property!")

    # endregion