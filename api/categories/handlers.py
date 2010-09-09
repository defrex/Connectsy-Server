

from base_handlers import BaseHandler
import json


class CategoriesHandler(BaseHandler):
    
    def get(self):
        self.output(
            [{'categories': [{'name': 'baseball'},
                            {'name': 'basketball'},
                            {'name': 'bike riding/cycling'},
                            {'name': 'boxing'},
                            {'name': 'football'},
                            {'name': 'gym/exercise'},
                            {'name': 'hockey'},
                            {'name': 'martial arts'},
                            {'name': 'skateboarding'},
                            {'name': 'soccer'},
                            {'name': 'tennis'},
                            {'name': 'ultimate'},
                            {'name': 'walk'},
                            {'name': 'other'}],
             'name': 'Sports & Leisure'},
            {'categories': [{'name': 'art show'},
                            {'name': 'blind date'},
                            {'name': 'casino/slots'},
                            {'name': 'casual hook-up'},
                            {'name': 'club'},
                            {'name': 'date'},
                            {'name': 'movie'},
                            {'name': 'nightlife'},
                            {'name': 'party'},
                            {'name': 'racetrack'},
                            {'name': 'other '}],
             'name': 'Entertainment '},
            {'categories': [{'name': 'bbq'},
                            {'name': 'breakfast'},
                            {'name': 'brunch'},
                            {'name': 'coffee or tea'},
                            {'name': 'dinner'},
                            {'name': 'drinks'},
                            {'name': 'lunch'},
                            {'name': 'snack'},
                            {'name': 'other '}],
             'name': 'Food & Drink '},
            {'categories': [{'categories': [{'name': 'backgammon'},
                                            {'name': 'chess'},
                                            {'name': 'monopoly'},
                                            {'name': 'scrabble'},
                                            {'name': 'other'}],
                             'name': 'board games'},
                            {'categories': [{'name': 'euchre'},
                                            {'name': 'poker'},
                                            {'name': 'other'}],
                             'name': 'card games'},
                            {'categories': [{'name': 'ps3'},
                                            {'name': 'wii'},
                                            {'name': 'xbox'},
                                            {'name': 'other '}],
                             'name': 'video games'}],
             'name': 'Games & Activites'}]
        )