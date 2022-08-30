from odoo import models, fields, api

class Oders(models.TransientModel):
    _name = 'orders'
    
    name = fields.Char(string='Name', readonly=True)
    product = fields.Char(string="Product", readonly=True)
    amount = fields.Integer(string="Amount", readonly=True)
    total_price = fields.Monetary(string="Total Price", readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency')
    dropout_reason = fields.Text(string='Dropout Reason')


class detail_order(models.TransientModel):
    _name = "detail.orders"
    _inherit = "orders"
    
    name = fields.Char("Name")
    address = fields.Char("Address", readonly=True)
    # address = fields.Char("Address", groups="Customer.group_admin")
    number = fields.Char("Number", readonly=True)
    

            
            
            
            
            
            
            