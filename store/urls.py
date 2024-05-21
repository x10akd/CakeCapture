from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("category/<str:cat>", views.category, name="category"),
    path("search/", views.search, name="search"),
    path("<pk>", views.product_detail, name="product_detail"),
    path("ajax-add-review/<int:pk>/", views.ajax_add_review, name="ajax_add_review"),
    path(
        "ajax-edit-review/<int:review_id>/",
        views.ajax_edit_review,
        name="ajax_edit_review",
    ),
    path(
        "load_more_reviews/<int:product_id>",
        views.load_more_reviews,
        name="load_more_reviews",
    ),
]
