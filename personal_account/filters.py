import django_filters
from datetime import datetime

from rest_framework import filters

from models.models import Income, Expense


class IncomesFilter(filters.FilterSet):

    date = django_filters.DateFromToRangeFilter(
            name="date",
            method="filter_group_by"
    )

    class Meta:
        model = Income
        fields = []

    def filter_group_by(self, queryset, name, value):
        start_date = datetime.date(value.start)
        end_date = datetime.date(value.stop)
        queryset = queryset.filter(
                date__range=[start_date, end_date])

        return queryset


class ExpensesFilter(filters.FilterSet):

    date = django_filters.DateFromToRangeFilter(
            name="date",
            method="filter_group_by"
    )

    class Meta:
        model = Expense
        fields = []

    def filter_group_by(self, queryset, name, value):
        start_date = datetime.date(value.start)
        end_date = datetime.date(value.stop)
        queryset = queryset.filter(
                date__range=[start_date, end_date])

        return queryset
