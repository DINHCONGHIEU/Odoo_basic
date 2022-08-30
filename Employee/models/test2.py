from odoo import models,fields, api

class test2(models.Model):

    _name = "test2"
    _inherits = {'test':'test2_id','employee':'employee_id'}
    
    name = fields.Char("Name")
    test2_id = fields.Many2one('test')
    employee_id = fields.Many2one('employee','test2')
    employee_id_2 = fields.Many2many('test','rel_test','name','nums')
    