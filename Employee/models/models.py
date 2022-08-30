from odoo import models, fields 

class employee(models.Model):
    _name = "employee"
    
    name = fields.Char(string="Name", required=True)
    birthday = fields.Date(string="Birthday")
    gender = fields.Selection([('male','Male'),('female','Female'),('other','Other')], 
                              default='male')
    address = fields.Char(string="Address")
    number = fields.Char(string="Number")
    position = fields.Selection([('manager','Manager'),('sales','Sales'),
                                 ('technician','Technician'),('security','Security')])
    image = fields.Binary(string="Image", attachment=True)
    salary = fields.Float(string="Salary", digits=(8,2))
    skill = fields.Float(string="Skill" )
    
   

    
    
    