from celery import shared_task

@shared_task
def check_order_payment_status(order_id):
    from .models import Order
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 'waiting_for_check':
            order.fail()  # 呼叫狀態轉換的方法
    except Order.DoesNotExist:
        pass

@shared_task
def check_order_unpaid_to_fail(order_id):
    from .models import Order
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 'unpaid':
            order.fail()
    except Order.DoesNotExist:
        pass
