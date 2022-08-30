from odoo import models, fields, api

class product(models.Model):
    _name = 'product'
    _description = "table product"
    
    
    name = fields.Char(string="Product Name", index=True)
    image = fields.Binary(string="Image", attachment=True)
    manufacturer = fields.Char(string="manufacturer")
    price = fields.Monetary(string="Price")
    promotion = fields.Boolean("Promotion", default=False)
    old_price = fields.Monetary(string="Old Price")
    stocking = fields.Boolean(string="Stocking", default=False)
    amount = fields.Integer(string="Amount", readonly= True)
    currency_id = fields.Many2one('res.currency', string='Currency', default=23)
    priority = fields.Selection([('0', 'Null'), ('1', 'Very Bad'), ('2', 'Bad'), 
                                 ('3', 'Normal'),('4','Good'),('5','Very Good')], 
                                 "Evaluate", default='0', compute="_compute_priority",store=True)
    evaluate = fields.Integer(string="Evaluate")
    total_value_evaluate = fields.Integer("total")
    customer_id = fields.Many2one(string='customer', ondelete="set null")


    @api.onchange('stocking')
    def _onchange_amount(self):
        for s in self:
            if s.stocking == False:
                s.amount = 0
    
    
    @api.depends('evaluate')
    def _compute_priority(self):
        for s in self:
            sum = int(s.total_value_evaluate/s.evaluate)
            s.priority = str(sum)
    
    
    def buy(self):
            return {
                'res_model':'customer',
                'type':'ir.actions.act_window',
                'view_mode':'form',
                'target':'new',
                'view_id':self.env.ref('Customer.customer_view_form').id,
                'context':{
                    'default_product':self.id,
                }   
            }
            

    def check(self):
        print(self.env['product'].search([('amount', '>', 0), ('promotion', '=', True)]))









    