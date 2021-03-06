from django.db.models.query_utils import refs_expression
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Expanse, Notes
from django.views.generic import CreateView
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse, response
from .forms import ExpanseForm, NotesForm
import json
from django.contrib import messages
import csv

"""view to display all the budgets"""
def project_list(request):
	display_all_budgets = Project.objects.all()
	return render(request,'budget/project_list.html',{'display_all_budgets': display_all_budgets})#returns budget webpage

"""view to delete and add new spending"""
def project_detail(request, project_slug):
	project = get_object_or_404(Project, slug=project_slug)
	if request.method == 'POST':
		form = ExpanseForm(request.POST or None)
		if form.is_valid():
			form.save()
	elif request.method == 'DELETE':
		id = json.loads(request.body)['id']
		expanse = get_object_or_404(Expanse, id=id)
		expanse.delete()
		return HttpResponse('')
	return render(request,'budget/project_detail.html',{'project':project, 'expanse_list': project.expanses.all(), 'form': ExpanseForm})	


"""view to create new budget"""
class ViewBudgets(CreateView):
	model = Project
	template_name = 'budget/add.html'
	fields = ('name', 'budget')# this fields are used to add the name of the budget and the budget itsefl
	"""this is to submit the form"""
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.save()

		return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
		return slugify(self.request.POST['name'])

"""notes page render"""
def notes(request):
	if request.method == 'POST':
		form = NotesForm(request.POST or None)
		if form.is_valid():
			form.save()
			all_notes = Notes.objects.all()
		return render(request, 'budget/notes.html', {'all_notes':all_notes})
	else:
		all_notes = Notes.objects.all()
		return render(request, 'budget/notes.html', {'all_notes':all_notes})

"""function to delete a note"""
def deleteNote(request,note_id):
	item = Notes.objects.get(pk=note_id)
	item.delete()
	messages.success(request, ('Note was delted'))
	return redirect('notes')

"""function to export spendings as a csv file"""

def exportSpendingCsv(request):
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Project', 'Name', 'Amount'])

	for spending in Expanse.objects.all().values_list('project', 'title', 'amount'):#getting all values and fields
		writer.writerow(spending)	
	response['Content-Disposition'] = 'attachment; filename="spendings.csv"'
	return response

def exportNotesCsv(request):
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Note'])

	for thingies in Notes.objects.all().values_list('note'):#getting all values and fields
		writer.writerow(thingies)	
	response['Content-Disposition'] = 'attachment; filename="notes.csv"'
	return response	