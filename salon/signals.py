
# signals.py

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import PayrollTurn, EmployeePayrollTurn
from django.db import models


@receiver(post_save, sender=PayrollTurn)
def payroll_turn_saved(sender, instance, created, **kwargs):
    # if created:
    #     print(f"New payroll_turn_saved {instance} created!")
    #     update_employeee_daily_total_turn_price(instance)
    # else:
    #     print(f"payroll_turn_saved {instance} updated!")
    #     update_employeee_daily_total_turn_price(instance)
    pass

@receiver(post_delete, sender=PayrollTurn)
def payroll_turn_deleted(sender, instance, **kwargs):
    # print(f"payroll_turn_deleted {instance} deleted!")
    update_employeee_daily_total_turn_price(instance.employee_payroll_turn.id)

def update_employeee_daily_total_turn_price(employee_payroll_turn_id):
    total_price = PayrollTurn.objects.filter(employee_payroll_turn=employee_payroll_turn_id).aggregate(
        total_price=models.Sum('price'))
    emp_payroll_turn = EmployeePayrollTurn.objects.get(
        id=employee_payroll_turn_id)
    emp_payroll_turn.total_price = total_price['total_price']
    emp_payroll_turn.save()
