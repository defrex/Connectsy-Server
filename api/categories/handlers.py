

from base_handlers import BaseHandler
import json


class CategoriesHandler(BaseHandler):
    
    def get(self):
        self.output(
            [
                {'name': 'Food & Drink'},
                {'name': 'Entertainment'},
                {'name': 'Sports & Leisure'},
                {'name': 'Games & Activities'},
                {'name': 'Everything Else'},
            ]
        )