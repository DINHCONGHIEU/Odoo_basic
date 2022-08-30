from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError, UserError
import re


class customer(models.AbstractModel):
    _name = 'table'

    name = fields.Char(string="Name")
    birthday = fields.Datetime(string="Birthday")
    address = fields.Char(string="Address")
    gender = fields.Selection([("male", "Male"), ("female", "Female")], string="Gender", default="male",)
    number = fields.Char(string="Number")

    def create_order(self):
        pass


class CustomerExtend(models.Model):
    _name = 'customer'
    _description = 'customers'
    _inherit = 'table'

    name = fields.Char(string="Name", required=True)
    birthday = fields.Date(string="Birthday")
    address = fields.Char(string="Address")
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ('other', 'Other')],
                              string="Gender", default="male",)
    number = fields.Char(string="Number")
    product = fields.Many2one("product", ondelete="set null")
    amount = fields.Integer(string="Amount", readonly=False)
    age = fields.Integer(string="Age", compute="_compute_age")
    currency_id = fields.Many2one('res.currency', string='Currency', default=23)
    total_price = fields.Monetary(string="Total Price", digits=(12, 2),
                                   currency_field='currency_id', compute="_compute_price", store=True)
    priority = fields.Selection([('0', 'Null'), ('1', 'Very Bad'), ('2', 'Bad'),
                                 ('3', 'Normal'), ('4', 'Good'), ('5', 'Very Good')],
                                 "Evaluate", default='0')
    product1 = fields.One2many('product', 'customer_id', string='Product')
    categories_money = fields.Selection([('vnd', 'VND'), ('usd', 'USD'), ('eur', 'EUR')],
                                        string="Categories Money", default="vnd")
    email_customer = fields.Char("Email customer")


    def copy_record(self, default=None):
        for s in self:
                new_name = s.name + " (copy)"
                s.copy({'name':new_name})

    def write_record_increase(self):
        for s in self:
            s.write({'amount':s.amount + 1})

    def write_record_reduce(self):
        for s in self:
            s.write({'amount':s.amount - 1})

    def browse_name_upper(self):
        result = self.browse([44, 45, 55])
        for s in result:
            s.name = s.name.upper()

    def filtered_name_title(self):
        names = self.filtered(lambda x: x.name.isupper())
        for s in names:
            s.name = s.name.title()

    def mapped_calculate_product_amount(self):
        a = self.filtered('product')
        results = {}
        for r in a:
            if results.get(r.product.name):
                results[r.product.name] += r.amount
            else:
                results.update({r.product.name:r.amount})
        for i in results:
            print("Number", i, "sold: ", results[i])
        print("Total number of products sold: ", sum(a.mapped('amount')))

    @api.onchange('product')
    def _onchange_product(self):
        for s in self:
            if s.product:
                s.product1 = s.product

    @api.depends('amount', 'categories_money', 'product')
    def _compute_price(self):
        pass

    def create_order(self):
        # orders = self.env['detail.orders'].create([{'name':self.name,
        #                                 'address':self.address,
        #                                 'number':self.number,
        #                                 'product':self.product.name,
        #                                 'amount':self.amount,
        #                                 'total_price':self.total_price}])
        return {
                'type':'ir.actions.act_window',
                'name':'Your Bill',
                'res_model':'detail.orders',
                'target':'new',
                'view_mode':'form',
                'context':{
                    'default_name':self.name,
                    'default_address':self.address,
                    'default_number':self.number,
                    'default_product':self.product.name,
                    'default_amount':self.amount,
                    'default_total_price':self.total_price,
                    'default_currency_id':self.currency_id.id,
                    }
                }

    @api.onchange('amount')
    def _onchange_amount(self):
        if self.amount > self.product.amount:
            raise ValidationError('Not enough products')
        else:
            self.product.amount -= self.amount

    def _compute_age(self):
        curent_year = fields.Date.today().year
        for r in self:
            if r.birthday and curent_year and r.birthday.year <= curent_year:
                r.age = curent_year - r.birthday.year
            else:
                r.age = 0

    @api.constrains('birthday')
    def _check_birthday(self): 
        for r in self:
            if r.birthday and r.birthday > fields.Date.today():
                raise ValidationError('Birthday must be in the past')

    @api.onchange('priority')
    def _onchange_evaluate(self):
        for s in self:
            if s.priority:
                s.product.evaluate += 1
                s.product.total_value_evaluate += int(s.priority)
                
    def show_appointments(self):
        pass

    def button_journal_entries(self):
        pass

    _sql_constraints = [("name", "UNIQUE('name')", "Name already exist!")]

    # @api.constrains('name')
    # def _check_name_unique(self):
    #     name_cnt = self.search_count([('name', '=', self.name), ('id', '!=', self.id)])
    #     if name_cnt > 0:
    #         raise ValidationError("Name already exists!")

    def action_url(self):
        return {
        'name': "Website",
        'type': 'ir.actions.act_url',
        'url': 'https://www.google.com/',
        # 'target': 'self',
        'target': 'new',
        }

    _sql_constraints = [('amount', 'CHECK(amount > 0)', "Amount must > 0!")]

    @api.constrains('email_customer')
    def _check_email(self):
        pattern = '[A-Za-z0-9]+@gmail.com'
        for s in self:
            if s.email_customer and not re.match(pattern, s.email_customer):
                raise ValidationError('Emaill Error!')

    _sql_constraints = [('email_customer', 'UNIQUE(email_customer)', 'Email Error!')]     



class employee_customer(CustomerExtend):

    def _compute_price(self):
        for s in self:
            if s.categories_money == "vnd" and s.amount:
                s.currency_id = 23
                price = s.amount * s.product.price
                s.total_price = price - float((price * 10) / 100)
            if s.categories_money == 'usd' and s.amount:
                s.currency_id = 2
                price = float((s.amount * s.product.price) / 23405.00)
                s.total_price = price - float((price * 10) / 100)
            if s.categories_money == 'eur' and s.amount:
                s.currency_id = 1
                price = float((s.amount * s.product.price) / 23812.72)
                s.total_price = price - float((price * 10) / 100)


class normal_customer(CustomerExtend):
    
    def _compute_price(self):
        for s in self:
            if s.categories_money == "vnd" and s.amount:
                s.currency_id = 23
                s.total_price = s.amount * s.product.price
            if s.categories_money == 'usd' and s.amount:
                s.currency_id = 2
                s.total_price = float((s.amount * s.product.price) / 23405.00)
            if s.categories_money == 'eur' and s.amount:
                s.currency_id = 1
                s.total_price = float((s.amount * s.product.price) / 23812.72)


        
