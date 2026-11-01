
from django.db import models
from django.conf import settings
from decimal import Decimal


class Branch(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название филиала"
    )
    address = models.CharField(
        max_length=250,
        verbose_name="Адрес"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Филиал"
        verbose_name_plural = "Филиалы"


class Client(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name="ФИО клиента"
    )
    address = models.CharField(
        max_length=250,
        verbose_name="Адрес"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"


class Agent(models.Model):
    full_name = models.CharField(
        max_length=200,
        verbose_name="ФИО агента"
    )
    address = models.CharField(
        max_length=250,
        verbose_name="Адрес"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Телефон"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Филиал"
    )

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Страховой агент"
        verbose_name_plural = "Страховые агенты"


class InsuranceType(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Вид страхования"
    )
    tariff_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Тарифная ставка (%)"
    )
    commission_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Процент комиссии (%)"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вид страхования"
        verbose_name_plural = "Виды страхования"


class Contract(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент"
    )
    agent = models.ForeignKey(
        Agent,
        on_delete=models.CASCADE,
        verbose_name="Страховой агент"
    )
    branch = models.ForeignKey(
        Branch,
        on_delete=models.CASCADE,
        verbose_name="Филиал"
    )
    insurance_type = models.ForeignKey(
        InsuranceType,
        on_delete=models.CASCADE,
        verbose_name="Вид страхования"
    )
    date = models.DateField(
        verbose_name="Дата заключения"
    )
    insurance_sum = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="Страховая сумма"
    )

    @property
    def insurance_payment(self):
        return (
            self.insurance_sum
            * self.insurance_type.tariff_rate
            / Decimal("100")
        )

    @property
    def agent_salary(self):
        return (
            self.insurance_payment
            * self.insurance_type.commission_percent
            / Decimal("100")
        )

    def __str__(self):
        return f"Договор №{self.id} — {self.client}"

    class Meta:
        verbose_name = "Договор страхования"
        verbose_name_plural = "Договоры страхования"


class Article(models.Model):
    title = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Название публикации"
    )
    text = models.TextField(
        verbose_name="Текст публикации"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Автор"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
