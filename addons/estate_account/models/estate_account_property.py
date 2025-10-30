from odoo import models, Command

class EstateAccountProperty(models.Model):
    _inherit = "estate.property"

    def sell_property(self):
        self.env['account.move'].create({
            'partner_id': self.buyer.id,
            'move_type': 'out_invoice',
            'line_ids': [
                Command.create({
                    'name': f'Commision for the sale of {self.name}',
                    'quantity': 1.0,
                    'price_unit': 6/100 * self.selling_price
                }),
                Command.create({
                    'name': f'Administrative fee for the sale of {self.name}',
                    'quantity': 1.0,
                    'price_unit': 100.00
                })
            ]
        })
        return super().sell_property()