from django.shortcuts import render
from django.http import HttpResponse

#Extra import for generic list and details views work
from django.views import generic
from .models import Student

# Create your views here.

def index(request):
   # Render index.html
   return render( request, 'portfolio_app/index.html')


#Update the views to use the generic list and details views
class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student
