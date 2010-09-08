

from base_handlers import BaseHandler
import json


class CategoriesHandler(BaseHandler):
    
    def get(self):
        self.write(json.dumps([
            {'categories': [{'name': 'baseball\n'},
                             {'name': 'basketball\n'},
                             {'name': 'bike riding/cycling\n'},
                             {'name': 'boxing\n'},
                             {'name': 'football\n'},
                             {'name': 'gym/exercise\n'},
                             {'name': 'hockey\n'},
                             {'name': 'martial arts\n'},
                             {'name': 'skateboarding\n'},
                             {'name': 'soccer\n'},
                             {'name': 'tennis\n'},
                             {'name': 'ultimate\n'},
                             {'name': 'walk\n'},
                             {'name': 'other\n'}],
              'name': 'Sports & Leisure\n'},
             {'categories': [{'name': 'art show\n'},
                             {'name': 'blind date\n'},
                             {'name': 'casino/slots\n'},
                             {'name': 'casual hook-up\n'},
                             {'name': 'club\n'},
                             {'name': 'date\n'},
                             {'name': 'movie\n'},
                             {'name': 'nightlife\n'},
                             {'name': 'party\n'},
                             {'name': 'racetrack\n'},
                             {'name': 'other \n'}],
              'name': 'Entertainment \n'},
             {'categories': [{'name': 'bbq\n'},
                             {'name': 'breakfast\n'},
                             {'name': 'brunch\n'},
                             {'name': 'coffee or tea\n'},
                             {'name': 'dinner\n'},
                             {'name': 'drinks\n'},
                             {'name': 'lunch\n'},
                             {'name': 'snack\n'},
                             {'name': 'other \n'}],
              'name': 'Food & Drink \n'},
             {'categories': [{'categories': [{'name': 'backgammon\n'},
                                             {'name': 'chess\n'},
                                             {'name': 'monopoly\n'},
                                             {'name': 'scrabble\n'},
                                             {'name': 'other\n'}],
                              'name': 'board games\n'},
                             {'categories': [{'name': 'euchre\n'},
                                             {'name': 'poker\n'},
                                             {'name': 'other\n'}],
                              'name': 'card games\n'},
                             {'categories': [{'name': 'ps3\n'},
                                             {'name': 'wii\n'},
                                             {'name': 'xbox\n'},
                                             {'name': 'other '}],
                              'name': 'video games\n'}],
              'name': 'Games & Activites\n'}
        ]))