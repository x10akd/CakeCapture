from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("", views.products_list, name="products_list"),
    path("category/<str:category>", views.category, name="category"),
    path("search/", views.search, name="search"),
    path("<pk>", views.product_detail, name="product_detail"),
    path("add-review/<int:pk>/", views.add_review, name="add_review"),
    path(
        "edit-review/<int:review_id>/",
        views.edit_review,
        name="edit_review",
    ),
    path(
        "load_more_reviews/<int:product_id>",
        views.load_more_reviews,
        name="load_more_reviews",
    ),
]
