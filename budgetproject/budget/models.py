from django.db import models
from django.utils.text import slugify

"""this is the model for project"""
class Project(models.Model):
    #name of the project
    name = models.CharField(max_length=100)
    #unique url created from name e.g(Hello world to hello=world)
    slug = models.SlugField(max_length=100,unique=True, blank=True)
    #the amount of money for the budget
    budget = models.IntegerField()

    #saving the budget
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Project, self).save(*args, **kwargs)
    #display the name in admin page
    def __str__(self):
        return self.name

    """function to subtract how much user spent"""
    def budget_spent(self):
        spending_list = Expense.objects.filter(project=self)
        total_spending_amount = 0
        for spending in spending_list:
            total_spending_amount += spending.amount
        return self.budget - total_spending_amount


"""This is the model for expenses"""
class Expense(models.Model):
    project = models.ForeignKey(Project, 
    on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.title

"""Model for Notes"""
class Notes(models.Model):
    note = models.CharField(max_length=200)

    def __str__(self):
        return self.note