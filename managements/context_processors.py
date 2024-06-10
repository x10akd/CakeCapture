from feedbacks.models import Feedback
from orders.models import Order


def no_reply_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        count = Feedback.objects.filter(reply__isnull=True).count()
        return {"no_reply_count": count}
    return {}


def new_order_count(request):
    if request.user.is_authenticated and request.user.is_superuser:
        count = Order.objects.filter(status="waiting_for_shipment").count()
        return {"new_order_count": count}
    return {}
