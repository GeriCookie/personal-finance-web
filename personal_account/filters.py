import django_filters 
from datetime import datetime
from django.db.models import F, Sum

from rest_framework import filters

from personal_account.models import Income, Expense, Category, Expense

class IncomesFilter(filters.FilterSet):

    date = django_filters.DateFromToRangeFilter(name="date", method="filter_group_by")

    class Meta:
        model = Income
        fields = []
    
    def filter_group_by(self, queryset, name, value):
        import ipdb; ipdb.set_trace()
        start_date = datetime.date(value.start)
        end_date = datetime.date(value.stop)
        queryset = queryset.filter(
            date__range=[start_date, end_date]).values('category__name').annotate(amount_per_category=Sum('amount'))

 
        return queryset
