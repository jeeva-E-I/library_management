from odoo import models, fields, api
class BookTag(models.Model):
    _name = 'library.book_tag'
    _description = 'Library Book'
    _order = 'sequence, id' # it is used to change the sequence number according to values, if we change the 3rd value to the first row means it will automatically moves according to the sequence

    
    name = fields.Char(string='Title', required=True) # tracking is true means, changes will be displayed in chatter
    sequence = fields.Integer(string="sequence", default="100")