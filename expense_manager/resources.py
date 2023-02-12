# core django
from django.contrib.auth.models import User

# project
from .models import Expense, Budget

# third party
from tastypie.resources import ModelResource
from tastypie.constants import ALL
from tastypie.authorization import DjangoAuthorization
from tastypie import fields

class BaseResource(ModelResource):
    def get_object_list(self, request):
        return super().get_object_list(request).filter(user=request.user)

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user
        return bundle

    def render_detail(self, request, pk):
        resp = self.get_detail(request, pk=pk)
        return resp.content

    def render_list(self, request):
        resp = self.get_list(request)
        return resp.content

class BudgetResource(BaseResource):
    class Meta:

        queryset = Budget.objects.all()
        resource_name = 'budget'
        authorization = DjangoAuthorization()
        filtering = {
            'budget': ALL,
            'month': ALL,
        }
        ordering = ['month']
        excludes = ('created', 'modified',)

class ExpenseResource(BaseResource):
    class Meta:
        queryset = Expense.objects.all()
        resource_name = 'expense'
        authorization = DjangoAuthorization()
        filtering = {
            'name': ALL,
            'price': ALL,
            'photo': ALL,
            'created': ['exact', 'range', 'gte']
        }
        ordering = ['name', 'price']
        excludes = ('modified',)