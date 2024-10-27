from math import isclose
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Target(models.Model):
    """ A betting target.
    A Target is a model, representing a betting target:
    A question
    Possible outcomes : List[Outcome]
    Resources
    """
    question = models.CharField(max_length=255)
    # A target can have multiple outcomes
    #possible_outcomes = models.ManyToManyField('Outcome', related_name='targets')
    resources = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    @property
    def possible_outcomes(self):
        """ Find all 'Outcomes' associated with this target
        """
        return Outcome.objects.filter(target=self)
    
    @property
    def num_bets(self):
        return sum([outcome.num_bets for outcome in self.possible_outcomes])
    
    @property
    def comments(self):
        return self.comment_set.all()
    
    @property
    def num_comments(self):
        return self.comment_set.count()
    
    def validate_outcomes(self):
        if self.possible_outcomes.count() < 2:
            raise ValidationError('A target must have at least 2 outcomes')
        if not isclose(sum([outcome.probability for outcome in self.possible_outcomes.all()]), 1):
            raise ValidationError('Sum of probabilities must be equal to 1')
        
    
    
class Outcome(models.Model):
    """ A possible outcome of a target.
    An Outcome is a model, representing a possible outcome of a target.
    Each outcome is associated with a target, and has
    - outcome,
    - description,
    - probability of happening,
    - history of Bets placed on it
    """
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    outcome = models.CharField(max_length=255)
    description = models.TextField()
    probability = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.outcome
    
    @property
    def betting_odd(self):
        return min(1/self.probability, 1000)
    
    @property
    def betting_odd_rounded(self):
        return round(self.betting_odd, 2)
    
    @property
    def num_bets(self):
        return self.bet_set.count()
    
    def validate_probability(self):
        if self.probability < 0 or self.probability > 1:
            raise ValidationError('Probability must be between 0 and 1')
    
    def save(self, *args, **kwargs):
        self.validate_probability()
        super(Outcome, self).save(*args, **kwargs)
        
class Comment(models.Model):
    """ A comment on a target.
    A Comment is a model, representing a comment on a target.
    Each comment is associated with a target, and has
    - user,
    - text,
    - created_at
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target = models.ForeignKey(Target, on_delete=models.CASCADE)
    text = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.target.question}'
        
class Bet(models.Model):
    """ A bet placed on an outcome.
    A Bet is a model, representing a bet that a user places on an outcome.
    Each bet is associated with a user, an outcome, and has
    - amount,
    - status (pending, won, lost, failed)
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    outcome = models.ForeignKey(Outcome, on_delete=models.CASCADE)
    amount = models.FloatField(default=1)
    status = models.CharField(max_length=255, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.user.username} - {self.outcome.outcome}'
    
    def validate_amount(self):
        if self.amount <= 0:
            raise ValidationError('Amount must be greater than 0')
    
    def save(self, *args, **kwargs):
        self.validate_amount()
        super(Bet, self).save(*args, **kwargs)