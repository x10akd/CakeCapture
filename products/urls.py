from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.all, name="all"),
    path("category/<str:category>", views.category, name="category"),
    path("search/", views.search, name="search"),
    path("<pk>", views.detail, name="detail"),
    path("add_review/<int:pk>/", views.add_review, name="add_review"),
    path("edit_review/<int:review_id>/", views.edit_review, name="edit_review"),
    path(
        "load_more_reviews/<int:product_id>",
        views.load_more_reviews,
        name="load_more_reviews",
    ),
    path("add_to_favorites/", views.add_to_favorites, name="add_to_favorites"),
]
