

from base_handlers import BaseHandler


class CategoriesHandler(BaseHandler):
    
    def get(self):
        self.write({
            'Entertainment \n': {'art show\n': None,
                                'blind date\n': None,
                                'casino/slots\n': None,
                                'casual hook-up\n': None,
                                'club\n': None,
                                'date\n': None,
                                'movie\n': None,
                                'nightlife\n': None,
                                'other \n': None,
                                'party\n': None,
                                'racetrack\n': None},
           'Food & Drink \n': {'bbq\n': None,
                               'breakfast\n': None,
                               'brunch\n': None,
                               'coffee or tea\n': None,
                               'dinner\n': None,
                               'drinks\n': None,
                               'lunch\n': None,
                               'other \n': None,
                               'snack\n': None},
           'Games & Activites\n': {'board games\n': {'backgammon\n': None,
                                                     'chess\n': None,
                                                     'monopoly\n': None,
                                                     'other\n': None,
                                                     'scrabble\n': None},
                                   'card games\n': {'euchre\n': None,
                                                    'other\n': None,
                                                    'poker\n': None},
                                   'video games\n': {'other ': None,
                                                     'ps3\n': None,
                                                     'wii\n': None,
                                                     'xbox\n': None}},
           'Sports & Leisure\n': {'baseball\n': None,
                                  'basketball\n': None,
                                  'bike riding/cycling\n': None,
                                  'boxing\n': None,
                                  'football\n': None,
                                  'gym/exercise\n': None,
                                  'hockey\n': None,
                                  'martial arts\n': None,
                                  'other\n': None,
                                  'skateboarding\n': None,
                                  'soccer\n': None,
                                  'tennis\n': None,
                                  'ultimate\n': None,
                                  'walk\n': None}
        })