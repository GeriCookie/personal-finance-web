from rest_framework import serializers

from models.models import Balance, Income, Expense, \
        Category, SavingsGoal, Budget


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(max_length=500)
    color = serializers.CharField(max_length=500)

    def create(self, validated_data):
        category_name = validated_data.pop('name')
        category_color = validated_data.pop('color')
        category = Category.objects.filter(name=category_name).first()
        if not category:
            category = Category.objects.create(name=category_name,
                    color=category_color)
        else:
            category.color = category_color
            category.save()
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
            category = Category.objects.create(name=category_data['name'],
                    color=category_data['color'])
        else:
            category.color = category_data['color']
            category.save()
        balance = self.context['request'].user.balance
        income = Balance.objects.create_income(
                category=category, balance=balance, **validated_data)
        return income


class IncomesByDatesSerializer(serializers.Serializer):
    category__name = serializers.ReadOnlyField()
    amount_per_category = serializers.ReadOnlyField()


class ExpensesByDatesSerializer(serializers.Serializer):
    category__name = serializers.ReadOnlyField()
    category__color = serializers.ReadOnlyField()
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
            category = Category.objects.create(name=category_data['name'],
                    color=category_data['color'])
        else:
            category.color = category_data['color']
            category.save()
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


class BudgetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Budget
        fields = ('id', 'amount', 'end_date', 'completed')

    def create(self, validated_data):
        balance = self.context['request'].user.balance
        budget = Balance.objects.create_budget(
                balance=balance, **validated_data)
        return budget


class BalanceSerializer(serializers.ModelSerializer):
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)
    savings_goals = SavingsGoalSerializer(many=True, read_only=True)
    budget = BudgetSerializer(many=True, read_only=True)

    class Meta:
        model = Balance
        fields = ('id', 'total_income', 'total_expense',
                  'total_amount', 'recommended_expenses_per_day',
                  'target_savings_budget_end', 'total_savings',
                  'remaining_budget', 'average_expenses_per_day',
                  'end_date_available_funds', 'incomes',
                  'expenses', 'savings_goals', 'budget')
