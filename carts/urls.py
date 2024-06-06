from django.urls import path
from . import views

app_name = "carts"


urlpatterns = [
    path("", views.summary, name="summary"),
    path("add/",views.add,name='add'),
    path("delete/",views.delete,name='delete'),
    path("deleteAll/",views.delete_all,name='delete_all'),
    path("update/",views.update,name='update'),
    path("rebuyonfail/<int:order_id>/", views.rebuyonfail, name="rebuyonfail"),
]
