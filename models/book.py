from odoo import models, fields, api
from datetime import date


today = date.today()
class Book(models.Model):
    _name = 'library.book'
    _inherit = ['mail.thread']
    _description = 'Library Book'
    # _rec_names_search = ['name','author_id'] # Not working .............(doubt)
    _rec_name = 'name'

    category_id = fields.Many2one('library.category', string= "Category") #here we used many-2-1 relation the category_id will have the category
    name = fields.Char(string='Title', required=True, tracking = True) # tracking is true means, changes will be displayed in chatter
    author_id = fields.Many2one('library.author',string='Author')
    isbn = fields.Char(string='ISBN', tracking = True)
    published_date = fields.Date(string='Published Date' ,tracking = True)
    description = fields.Text(string='Description', tracking = True)

    display_name = fields.Char(compute='_compute_display_name', store=True) # Not working ..............(doubt)

    tag_ids = fields.Many2many('library.book_tag') # defining many2many relation by adding book_tags model name, if we specify this field it looks like a tree structure.
    # You wil not see this field in the table, it will create a new table 
    def duplicate_record(self):
        for record in self: 
            self.env['library.book'].create({ #env creates enivornment for accesing the models, ids , queries
                'name': record.name,
                'category_id':record.category_id.id, # if we use many2one we need to specify the .id
                'author_id': record.author_id.id,
                'isbn'  : record.isbn,
                'published_date' : today,
                'description' : record.description if record.description else 'Unknown'
            })

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = f" {rec.name} [{rec.author_id}]"

#In order establish one to many relationship we need to add another model
class BookAuthor(models.Model):
    _name = 'library.author'
    _description = 'Book author'
    _inherit = ['mail.thread']
    _rec_name = 'name'

    reference = fields.Char(string='Reference', default= 'New')
    name = fields.Char(string='Author Name', required=True)
    author_ids = fields.One2many('library.book', 'author_id', string="Books")
    dob = fields.Date(string="DOB")

    @api.model_create_multi
    def create(self, val_list):
        for vals in val_list:
            if not vals.get('reference') or vals['reference'] == 'New':
                vals['reference'] = self.env['ir.sequence'].next_by_code('library.author')
        return super().create(val_list)
    
