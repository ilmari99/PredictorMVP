from django.shortcuts import render, get_object_or_404
from .models import Prediction
# To handle user predictions (e.g., placing a bet)
from django.http import JsonResponse
from .models import Outcome, UserPrediction
from django.contrib.auth.decorators import login_required

def prediction_list(request):
    predictions = Prediction.objects.prefetch_related('outcomes').all()
    return render(request, 'predictions/prediction_list.html', {'predictions': predictions})

@login_required
def place_prediction(request):
    if request.method == 'POST':
        outcome_id = request.POST.get('outcome_id')
        amount = request.POST.get('amount')
        outcome = get_object_or_404(Outcome, id=outcome_id)
        
        user_prediction = UserPrediction.objects.create(
            user=request.user,
            outcome=outcome,
            amount=amount
        )
        return JsonResponse({'status': 'success', 'message': 'Prediction placed!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})
