from odoo import models, fields, api


class BookUpload(models.Model):
    _name = 'library.upload'
    _inherit = ['mail.thread']
    _description = 'Library Upload'
    _rec_name = 'category_id'    

    book_name = fields.Char(string='Book Name', required= True)
    category_id = fields.Many2one('library.category', string= "Category")
    description = fields.Text(string= "Description")
    # status = fields.Char(string='status', compute = "_compute_status", store=True) # while using compute it will not store in db so it we need to give store True

    author_id = fields.Many2one('library.author' ,string="Author Name", ondelete="restrict") #

    reference = fields.Char(related='author_id.reference') # By using related field we can able to get the value from the many2one model by using model.fieldname
    # this reference field will not be stored if we want to store means we need to use store = True

    # Selection is used to give dropdown 
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), 
                              ('published', 'Published'), ('cancel', 'Cancelled')], default = 'draft', tracking=True)


    def action_confirm (self): #self refers to current record
        for rec in self:
            if rec.state == 'draft':
                rec.state = "confirmed"
            elif rec.state == 'confirmed':
                rec.state = 'ongoing'
            elif rec.state == 'ongoing':
                rec.state = 'published'

    def action_cancel (self):
        for rec in self:
            rec.state = 'cancel'
    
    @api.depends('state')
    def _compute_status(self):
        for record in self:
            record.status =  record.state 
    
