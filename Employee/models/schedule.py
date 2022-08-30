from odoo import models, fields, api 
from datetime import datetime, timezone
from datetime import timedelta
import time


class schedule(models.TransientModel):
    _name = 'schedule' 
    
    name = fields.Many2one('employee', ondelete="cascade", string="Name", required=True)
    number = fields.Char("Number", compute="_compute_number", store=True)
    reason = fields.Char("Reason", required=True)
    shift = fields.Selection([('shift_0','All day'),('shift_1','7h30-12h'),
                            ('shift_2','13h-17h30'),('shift_3','Options')], 
                            default="shift_0", string="Shift")
    start = fields.Datetime("Date start", 
                            default=lambda *a: time.strftime('%Y-%m-%d 00:00:00'))
    stop = fields.Datetime("Date stop", 
                           default=lambda *a: time.strftime('%Y-%m-%d 00:00:00'))
    time_start = fields.Float(string='start')
    time_stop = fields.Float(string='stop')

    
    
    @api.depends('name')
    def _compute_number(self):
        for s in self:
            if s.name:
                s.number = s.name.number
    
    
    @api.onchange('shift','time_start','time_stop')
    def _onchange_shift(self):
        for s in self:
            if s.shift == 'shift_0':
                s.start = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.stop = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.start += timedelta(hours=0.5)
                s.stop += timedelta(hours=10.5)
            elif s.shift == 'shift_1':
                s.start = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.stop = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.start += timedelta(hours=0.5)
                s.stop += timedelta(hours=5)
            elif s.shift == 'shift_2':
                s.start = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.stop = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.start += timedelta(hours=6)
                s.stop += timedelta(hours=10.5)
            else :
                s.start = datetime.utcnow().replace(hour=0, minute=0, second=0)
                s.stop = datetime.utcnow().replace(hour=0, minute=0, second=0)
                a = int((s.time_start - 7) // 1)
                b = int((s.time_stop - 7) // 1)
                x = str("%.2f" % s.time_start).split('.')
                y = str("%.2f" % s.time_stop).split('.')
                c = int(x[1])
                d = int(y[1])
                s.start = s.start + timedelta(hours=a, minutes=c)
                s.stop = s.stop + timedelta(hours=b, minutes=d)
                

    
    
