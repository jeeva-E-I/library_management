from odoo import models, fields, api, _
from odoo.exceptions import UserError


class BookUpload(models.Model):
    _name = 'library.upload'
    _inherit = ['mail.thread']
    _description = 'Library Upload'
    _rec_name = 'category_id'    

    #Book details field
    book_name = fields.Char(string='Book Name', required= True)
    category_id = fields.Many2one('library.category', string= "Category")
    description = fields.Text(string= "Description")
    # status = fields.Char(string='status', compute = "_compute_status", store=True) # while using compute it will not store in db so it we need to give store True
    author_id = fields.Many2one('library.author' ,string="Author Name", ondelete="restrict") # On delete restrict is used to avoid null to the fields defined in another module, cascade to delete rec from every modules


    # auto increment field
    reference = fields.Char(related='author_id.reference') # By using related field we can able to get the value from the many2one model by using model.fieldname
    # this reference field will not be stored if we want to store means we need to use store = True


    # Selection is used to give dropdown 
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('ongoing', 'Ongoing'), 
                              ('published', 'Published'), ('cancel', 'Cancelled')], default = 'draft', tracking=True)

    # currency field (odoo supports default currency_id )
    my_currency_id = fields.Many2one("res.currency", default=20) 
    # currency_id = fields.Many2one("res.currency",default=20) # In default we should specify the id of the currency field    
    amount = fields.Monetary("Amount", currency_field="my_currency_id", ) # this will through you error if you are not defined with currency_id and also enable the currencies which will be hidden for some users
    """
    Whenever we define a monetary field it checks for default currency_id field available, if not means it won't show the symbol
    if currency_id is not used means we should we can define manually , and should specify in a monetary field
    http://localhost:8069/web#action=66&model=res.currency&view_type=list&cids=1 # use the above link for the enable different currency 
    """
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

    def unlink(self): # this method will be triggered when we delete a data in the model 
        for record in self:
            if record.state == 'confirmed' or record.state == "ongoing" or record.state == "published":
                raise UserError(_("You cannot delete confirmed records.")) # this will raise a error message , "_" is used to translate the error msg according to the user specified lang
        return super().unlink()
    
