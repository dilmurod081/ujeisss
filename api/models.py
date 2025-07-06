from django.db import models


class Player(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)  # In a real app, use Django's User model for security
    coins = models.IntegerField(default=0)
    achievement_sent = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Message(models.Model):
    player = models.ForeignKey(Player, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.player.username}"
