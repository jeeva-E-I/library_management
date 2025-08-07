# library_management/__manifest__.py acts like a metadata declaration
{
    'name': 'Library Management',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Manage Library Books',
    'description': 'A simple module to manage books in a library.',
    'depends': ['mail','product'],
    'data': [
        'security/ir.model.access.csv', # data field contains xml,csv files to load
        'data/sequence.xml',    
        'views/books_readonly.xml',
        'views/book_author.xml',
        'views/books_category.xml',
        'views/books_upload.xml',
        'views/book_tag_views.xml',
        'views/book_views.xml'  
        
    ],
    'installable': True, # if false means can't install via UI
    'images': ['addons/library_management/static/description/icon.png'],
    'application': True,
}
