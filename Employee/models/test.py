from odoo import models, fields, api


class test(models.Model):

    _name = "test"
    # _rec_name = 'nums'            #tên đại diện cho bản ghi khi hiển thị giao diện form, nếu ko có cả trường name và _rec_name ->tên hiển thị là recordset với id của bản ghi
    _order = 'unit_price'           #Sắp xếp trên view theo unit_price.mặc định sắp xếp theo id 

    name = fields.Char(" The product name ", required=True) 
    nums = fields.Integer(" Number ")
    unit_price = fields.Float(" Unit price of product ", digits=(8,2))
    all_price = fields.Float(" Total product price ", compute="_compute_all_price", store=False)
    nums_related = fields.Integer("Nums related",related="nums",readonly=False)
    related_select = fields.Reference(selection=[('employee','employee'),('product','product')])
    introduce_yourself = fields.Html("HTML")
    state = fields.Selection([
       ('draft', 'Draft'),
       ('in_progress', 'In Progress'),
       ('cancel', 'Cancelled'),
       ('done', 'Done'),
   ], default='draft')
    # message_follower_ids = fields.Char(default="1")
    # activity_ids = fields.Char(default="1")
    # message_ids = fields.Char(default="1")
    

    
    def button_in_progress(self):
        self.write({
           'state': "in_progress"
        })
    
    
    def _compute_all_price(self):
        for s in self:
            s.all_price = s.unit_price * s.nums
        return {'context':{'name':'Hello'}}
    
    def check(self):
        print(self.name_get())
    
    def show_appointments(self):
        pass
            
    def button_journal_entries(self):
        pass








            