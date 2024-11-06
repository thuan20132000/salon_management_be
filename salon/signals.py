
# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PayrollTurn, EmployeePayrollTurn
from django.db import models


@receiver(post_save, sender=PayrollTurn)
def payroll_turn_saved(sender, instance, created, **kwargs):
    if created:
        print(f"New payroll_turn_saved {instance} created!")
        update_employeee_daily_total_turn_price(instance)
    else:
        print(f"payroll_turn_saved {instance} updated!")
        update_employeee_daily_total_turn_price(instance)


def update_employeee_daily_total_turn_price(payroll_turn):
    total_price = PayrollTurn.objects.filter(employee_payroll_turn=payroll_turn.employee_payroll_turn.id).aggregate(
        total_price=models.Sum('price'))
    emp_payroll_turn = EmployeePayrollTurn.objects.get(
        id=payroll_turn.employee_payroll_turn.id)
    emp_payroll_turn.total_price = total_price['total_price']
    emp_payroll_turn.save()
