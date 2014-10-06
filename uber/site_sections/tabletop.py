from uber.common import *

@all_renderable(CHECKINS)
class Root:
    @property
    def attendees(self):
        return [{
            'id': a.id,
            'name': a.full_name,
            'badge': a.badge_num
        } for a in Attendee.objects.exclude(badge_num=0).order_by('badge_num')]
    
    @property
    def games(self):
        return [g.to_dict() for g in Game.objects.order_by('name').select_related()]
    
    #@ng_renderable
    def index(self):
        return {
            'games': json.dumps(self.games, cls=serializer),
            'attendees': json.dumps(self.attendees, cls=serializer),
        }
    
    @ajax
    def badged_attendees(self):
        return self.attendees

    @ajax
    def add_game(self, code, name, attendee_id):
        Game.objects.create(code=code, name=name, attendee_id=attendee_id)
        return {
            'message': 'Success!',
            'games': self.games
        }
    
    @ajax
    def checkout(self, game_id, attendee_id):
        Checkout.objects.create(game_id=game_id, attendee_id=attendee_id)
        return {
            'message': 'Success!',
            'games': self.games
        }
    
    @ajax
    def returned(self, game_id):
        Checkout.objects.get(game_id=game_id).delete()
        return {
            'message': 'Success!',
            'games': self.games
        }
    
    @ajax
    def return_to_owner(self, id):
        game = Game.get(id)
        game.returned = True
        game.save()
        return {
            'message': 'Success!',
            'games': self.games
        }
