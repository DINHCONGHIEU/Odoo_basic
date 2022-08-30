
#
# from odoo import http
# from odoo.http import request
#
# class Customer(http.Controller):        #kế thừa từ odoo.http.Controllers
#     @http.route('/customer/',type='http',auth='public') #route báo cho hệ thống biết là có một phương thức có thể truy cập trên web
#                                                         #auth hạn chế quyền truy cập vào dường dẫn
#     def index(self,*kw):
#
#         customer = request.env['customer'].sudo().search([])
#         html_result = '<html><body><ol>'
#         for c in customer:
#             html_result += "<li> %s - %s - %s</li>" % (c.name,c.address,c.number)
#         html_result += '</ol></body></html>'
#         return html_result

