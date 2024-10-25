from django.db import models
from django.contrib.auth.models import User

class Prediction(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    resources = models.TextField(help_text="Comma-separated URLs for resources", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Outcome(models.Model):
    prediction = models.ForeignKey(Prediction, related_name='outcomes', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    probability = models.FloatField(help_text="Current probability percentage")
    odds = models.FloatField(help_text="Payout odds")

    def __str__(self):
        return f"{self.name} ({self.probability}%)"

class UserPrediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.outcome.name}"
