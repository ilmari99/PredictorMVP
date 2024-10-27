from math import isclose
from django import forms
from django.forms import modelformset_factory
from .models import Target, Outcome

class TargetForm(forms.ModelForm):
    class Meta:
        model = Target
        fields = ['question', 'resources']
        widgets = {
            'resources': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean(self):
        cleaned_data = super().clean()
        possible_outcomes = cleaned_data.get('possible_outcomes')

        if possible_outcomes and possible_outcomes.count() < 2:
            raise forms.ValidationError('A target must have at least 2 outcomes')

        if possible_outcomes and not isclose(sum([outcome.probability for outcome in possible_outcomes]), 1):
            raise forms.ValidationError('Sum of probabilities must be equal to 1')

        return cleaned_data

class OutcomeForm(forms.ModelForm):
    class Meta:
        model = Outcome
        fields = ['outcome', 'description', 'probability']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }

    def clean_probability(self):
        probability = self.cleaned_data.get('probability')
        if probability < 0 or probability > 1:
            raise forms.ValidationError('Probability must be between 0 and 1')
        return probability
    
OutcomeFormSet = modelformset_factory(Outcome, form=OutcomeForm, extra=2)