from django.db import models
from core.models import Student, Collaboration

class Message(models.Model):
    text = models.TextField()
    read = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="messages")
    collaboration = models.ForeignKey(Collaboration, on_delete=models.CASCADE)
