from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

# Extra import for generic list and details views work
from django.views import generic
from .models import *

# Extra import for form
from .forms import *
from django.views import View
from django.contrib import messages

# Create your views here.

# Update view for index to pass all the portfolio objects that are active. Notice the print method used to see the query set results that will be passed


def index(request):
    student_active_portfolios = Student.objects.select_related(
        'portfolio').all().filter(portfolio__is_active=True)
    print("active portfolio query set", student_active_portfolios)
    return render(request, 'portfolio_app/index.html', {'student_active_portfolios': student_active_portfolios})


# Update the views to use the generic list and details views
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

# for project


class ProjectListView(generic.ListView):
    model = Project


class ProjectDetailVIew(generic.DetailView):
    model = Project


def createProject(request, portfolio_id):
    form = ProjectForm()
    portfolio = Portfolio.objects.get(pk=portfolio_id)

    if request.method == 'POST':
        # Create a new dictionary with form data and portfolio_id
        project_data = request.POST.copy()
        project_data['portfolio_id'] = portfolio_id

        form = ProjectForm(project_data)
        if form.is_valid():
            # Save the form without committing to the database
            project = form.save(commit=False)
            # Set the portfolio relationship
            project.portfolio = portfolio
            project.save()

            # Redirect back to the portfolio detail page
            return redirect('portfolio-detail', portfolio_id)

    context = {'form': form}
    return render(request, 'portfolio_app/project_form.html', context)

class DeleteProjectView(View):
    template_name = 'portfolio_app/delete_project.html'

    def get(self, request, portfolio_id, project_id):
        form = DeleteProjectForm()
        return render(request, self.template_name, {'form': form, 'portfolio_id': portfolio_id, 'project_id': project_id})

    def post(self, request, portfolio_id, project_id):
        form = DeleteProjectForm(request.POST)

        if form.is_valid() and form.cleaned_data['confirmation']:
            project = Project.objects.get(pk=project_id)
            project.delete()
            messages.success(request, 'Project deleted successfully.')
            return redirect('portfolio-detail', portfolio_id)

        messages.error(request, 'Project deletion failed. Please confirm the deletion.')
        return render(request, self.template_name, {'form': form, 'portfolio_id': portfolio_id, 'project_id': project_id})

class UpdateProjectView(View):
    template_name = 'portfolio_app/update_project.html'

    def get(self, request, portfolio_id, project_id):
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(instance=project)
        return render(request, self.template_name, {'form': form, 'portfolio_id': portfolio_id, 'project_id': project_id})

    def post(self, request, portfolio_id, project_id):
        project = get_object_or_404(Project, pk=project_id)
        form = ProjectForm(request.POST, instance=project)

        if form.is_valid():
            form.save()
            messages.success(request, 'Project updated successfully.')
            return redirect('portfolio-detail', portfolio_id)

        messages.error(request, 'Project update failed. Please check the form data.')
        return render(request, self.template_name, {'form': form, 'portfolio_id': portfolio_id, 'project_id': project_id})
