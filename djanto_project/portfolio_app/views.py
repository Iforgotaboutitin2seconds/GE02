from django.shortcuts import render
from django.http import HttpResponse

#Extra import for generic list and details views work
from django.views import generic
from .models import *

# Create your views here.

#Update view for index to pass all the portfolio objects that are active. Notice the print method used to see the query set results that will be passed
def index(request):
    student_active_portfolios = Student.objects.select_related('portfolio').all().filter(portfolio__is_active=True)
    print("active portfolio query set", student_active_portfolios)
    return render( request, 'portfolio_app/index.html', {'student_active_portfolios':student_active_portfolios})



#Update the views to use the generic list and details views
class StudentListView(generic.ListView):
    model = Student
class StudentDetailView(generic.DetailView):
    model = Student

# for Portfolio
class PortfolioDetailView(generic.DetailView):
    model = Portfolio

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Include the list of projects for the current portfolio
        context['projects'] = Project.objects.filter(portfolio=self.object)
        return context

#for project
class ProjectListView(generic.ListView):
    model = Project
class ProjectDetailVIew(generic.DetailView):
    model = Project