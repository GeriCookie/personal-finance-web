from rest_framework import serializers
from personal_account.models import Balance, Income, Expense, Category, \
                                                    SavingsGoal


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)

    def create(self, validated_data):
        category_name = validated_data.pop('name')
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name)
        return category


class IncomeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Income
        fields = ('id', 'category', 'amount', 'date')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.filter(name=category_data['name']).first()
        if not category:
            category = Category.objects.create(name=category_data['name'])
        print(self.context['request'].user)
        balance = self.context['request'].user.balance
        income = Balance.objects.create_income(
                category=category, balance=balance, **validated_data)
        return income


class IncomesByDatesSerializer(serializers.Serializer):
    category__name = serializers.ReadOnlyField()
    amount_per_category = serializers.ReadOnlyField()


class ExpensesByDatesSerializer(serializers.Serializer):
    category__name = serializers.ReadOnlyField()
    amount_per_category = serializers.ReadOnlyField()


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Expense
        fields = ('id', 'category', 'amount', 'date')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        category = Category.objects.filter(name=category_data['name']).first()
        if not category:
            category = Category.objects.create(name=category_data['name'])
        balance = self.context['request'].user.balance
        expense = Balance.objects.create_expense(
                category=category, balance=balance, **validated_data)
        return expense


class SavingsGoalSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingsGoal
        fields = ('id', 'amount', 'end_date', 'completed')

    def create(self, validated_data):
        balance = self.context['request'].user.balance
        savings_goal = Balance.objects.create_savings_goal(
                balance=balance, **validated_data)
        return savings_goal


class BalanceSerializer(serializers.ModelSerializer):
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    savings_goals = SavingsGoalSerializer(many=True, read_only=True)

    class Meta:
        model = Balance
        fields = ('id', 'total_income', 'total_expense',
                  'total_amount', 'recommended_expenses_per_day',
                  'target_savings_month_end', 'total_savings',
                  'incomes', 'expenses', 'savings_goals')
