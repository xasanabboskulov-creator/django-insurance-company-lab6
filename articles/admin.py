
from django.contrib import admin
from .models import Branch, Client, Agent, InsuranceType, Contract, Article


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'address', 'phone')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'address', 'phone')


@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'phone', 'branch')


@admin.register(InsuranceType)
class InsuranceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tariff_rate', 'commission_percent')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'client',
        'agent',
        'branch',
        'insurance_type',
        'date',
        'insurance_sum',
        'show_insurance_payment',
        'show_agent_salary',
    )

    @admin.display(description='Страховая выплата')
    def show_insurance_payment(self, obj):
        return obj.insurance_payment

    @admin.display(description='Зарплата агента')
    def show_agent_salary(self, obj):
        return obj.agent_salary


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'author')
    search_fields = ('title', 'text')
