from odoo import api, fields, models
from odoo.exceptions import ValidationError


class TestMateria(models.Model):
    _name = "test.material"
    _description = "Material"

    material_code = fields.Char(string='Material Code', required=True)
    name = fields.Char(string='Material Name', required=True)
    material_type = fields.Selection([
        ('fabric', 'Fabric'),
        ('jeans', 'Jeans'),
        ('cotton', 'Cotton')
    ], string='Material Type', required=True)
    buy_price = fields.Float(string='Buy Price', required=True)
    supplier_id = fields.Many2one('res.partner', string='Supplier', required=True)

    @api.constrains('buy_price')
    def _check_buy_price(self):
        for rec in self:
            if rec.buy_price < 100:
                raise ValidationError("Buy price must be at least 100.")