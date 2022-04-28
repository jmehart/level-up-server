from django.db import models

class Game(models.Model):
    # CASCADE will instruct Django to cascade the deleting effect 
    # i.e. delete all the Game model instances that depend on the Gamer model instance you deleted.
    game_type = models.ForeignKey("GameType", on_delete=models.CASCADE)
    title = models.CharField(max_length=55)
    maker = models.CharField(max_length=55)
    gamer = models.ForeignKey("Gamer", on_delete=models.CASCADE)
    number_of_players = models.IntegerField()
    skill_level = models.IntegerField()