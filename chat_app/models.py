"""
All the models of the apps are listed here.
"""
from django.db import models

class User(models.Model):
    AGENT="AGENT"
    CLIENT="CLIENT"
    Role = ((AGENT, "agent"),
            (CLIENT, "client"))
    username = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    role = models.CharField(max_length=100, choices=Role)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    deleted_at = models.DateTimeField(null=True)

class Thread(models.Model):
    LOAN=1
    PAYMENT=2
    OTHER=3
    Context = ((LOAN,"loan"), 
               (PAYMENT, "payment"), 
               (OTHER, "other"))
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent", null=True)
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="client")
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True)
    thread_type = models.PositiveSmallIntegerField(choices=Context)
    count = models.PositiveSmallIntegerField()

class Message(models.Model):
    message_body = models.TextField()
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender")
    timestamp = models.DateTimeField(auto_now_add=True)
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="thread")
    is_read = models.BooleanField(default=False)

