from django.shortcuts import render

# Create your views here.
def market_live_view(request):
    return render(request, 'market_live.html')