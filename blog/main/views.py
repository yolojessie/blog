from django.shortcuts import render

# Create your views here.


def main(request):
    '''
    Render the main page
    '''
    import datetime
    now = datetime.datetime.now()
    context = {'like':'Django 很棒','now':now}
    return render(request, 'main/main.html', context)

def about(request):
    '''
    Render the about page
    '''
    return render(request, 'main/about.html')