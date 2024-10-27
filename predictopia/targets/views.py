from django.shortcuts import render, get_object_or_404, redirect
# To handle user predictions (e.g., placing a bet)
from django.http import JsonResponse
from .models import Outcome,Target
from django.contrib.auth.decorators import login_required
from .forms import TargetForm, OutcomeFormSet

def index(request):
    """ Display a list of predictions
    """
    # Fetch ALL targets, and display them on the front page
    targets = Target.objects.all()
    return render(request, 'targets/index.html', {'targets': targets})

def add_target(request):
    if request.method == 'POST':
        target_form = TargetForm(request.POST)
        outcome_formset = OutcomeFormSet(request.POST, queryset=Outcome.objects.none())

        if target_form.is_valid() and outcome_formset.is_valid():
            target = target_form.save()
            for form in outcome_formset:
                outcome = form.save(commit=False)
                outcome.target = target
                outcome.save()
            return redirect('index')
    else:
        target_form = TargetForm()
        outcome_formset = OutcomeFormSet(queryset=Outcome.objects.none())

    return render(request, 'targets/add_target.html', {
        'target_form': target_form,
        'outcome_formset': outcome_formset,
    })

def target_view(request, target_id):
    """ Go to a specific target's page
    """
    target = get_object_or_404(Target, pk=target_id)
    return render(request, 'targets/target.html', {'target': target})
