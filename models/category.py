from odoo import models, fields, api


class BookCategory(models.Model):
    _name = 'library.category'
    _inherit = ['mail.thread']
    _description = 'Library Category'
    _rec_name = 'category' # it is used for showing the record name if not mentioned shows modelname + id

    reference = fields.Char(string='Reference', default= 'New')
    category = fields.Char(string='Category')
    description = fields.Text(string= "Description")
    

    @api.model_create_multi
    def create(self, val_list):
        for vals in val_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('library.category')
        return super().create(val_list)
    


