from django.db.models.query_utils import refs_expression
from django.shortcuts import render, get_object_or_404, redirect
from .models import Project, Expense, Notes
from django.views.generic import CreateView
from django.utils.text import slugify
from django.http import HttpResponseRedirect, HttpResponse, response
from .forms import ExpenseForm, NotesForm
import json
from django.contrib import messages
import csv

"""view to display all the budgets"""
def project_list(request):
	display_all_budgets = Project.objects.all()
	return render(request,'budget/project_list.html',
	#returns budget webpage
	{'display_all_budgets': display_all_budgets})

"""view to delete and add new spending"""
def project_detail(request, project_slug):
	project = get_object_or_404(Project, slug=project_slug)
	if request.method == 'POST':
		form = ExpenseForm(request.POST or None)
		if form.is_valid():
			form.save()
	elif request.method == 'DELETE':
		id = json.loads(request.body)['id']
		expense = get_object_or_404(Expense, id=id)
		expense.delete()
		return HttpResponse('')
	return render(request,'budget/project_detail.html',{'project':project, 
	'expense_list': project.expenses.all(), 'form': ExpenseForm})	


"""view to create new budget"""
class ViewBudgets(CreateView):
	model = Project
	template_name = 'budget/add.html'
	# this fields are used to add 
	# the name of the budget and the budget itsefl
	fields = ('name', 'budget')
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
		return render(request, 'budget/notes.html', 
		{'all_notes':all_notes})
	else:
		all_notes = Notes.objects.all()
		return render(request, 'budget/notes.html', 
		{'all_notes':all_notes})

"""view to delete a note"""
def deleteNote(request,note_id):
	item = Notes.objects.get(pk=note_id)
	item.delete()
	return redirect('notes')

"""view to export spendings as a csv file"""
def exportSpendingCsv(request):
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Name', 'Amount'])
	#getting all values and fields
	for spending in Expense.objects.all().values_list('title', 'amount'):
		writer.writerow(spending)	
	response['Content-Disposition'] = 'attachment; filename="spendings.csv"'
	return response

"""view to export notes as a csv file"""
def exportNotesCsv(request):
	response = HttpResponse(content_type='text/csv')
	writer = csv.writer(response)
	writer.writerow(['Note'])
	#getting all values and fields
	for thingies in Notes.objects.all().values_list('note'):
		writer.writerow(thingies)	
	response['Content-Disposition'] = 'attachment; filename="notes.csv"'
	return response	