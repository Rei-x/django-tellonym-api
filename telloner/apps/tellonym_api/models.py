from django.db import models
from .utils import hash_text

class TellonymUser(models.Model):
    hashed_username = models.CharField(max_length=64, unique=True)
    hashed_token = models.CharField(max_length=200, unique=True)
    @classmethod
    def create(cls, username, token):
        hashed_username = hash_text(username)
        hashed_token = hash_text(token)
        user = cls(hashed_username=hashed_username, hashed_token=hashed_token)
        user.save()
        return user

    def add_tells(self, tells):
        tellonym_array = []
        for tell in tells:
            tellonym_array.append(Tellonym(user=self, id=tell.id, text=tell.text))
        self.tellonym_set.bulk_create(tellonym_array, ignore_conflicts=True)



class Tellonym(models.Model):
    STATES = [
        ('NEW', 'Nowy'),
        ('ACCEPTED', 'Pobrany'),
        ('DISCARDED', 'Odrzucony')
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(TellonymUser, on_delete=models.CASCADE)
    text = models.CharField(max_length=500)
    state = models.CharField(max_length=15, choices=STATES, default='NEW')
