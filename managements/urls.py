from django.urls import path
from . import views

app_name = "managements"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("edit_product/<int:pk>/", views.edit_product, name="edit_product"),
    path("add_product/", views.ProductCreateView.as_view(), name="add_product"),
    path("category_list/", views.category_list, name="category_list"),
    path("add_category/", views.CategoryCreateView.as_view(), name="add_category"),
    path("edit_category/<int:pk>/", views.edit_category, name="edit_category"),
    path("quantity_index/", views.quantity_index, name="quantity_index"),
    path("quantity_charts/", views.quantity_charts, name="quantity_charts"),
    path("quantity_alter/<str:category>/", views.quantity_alter, name="quantity_alter"),
    path("coupon_list", views.coupon_list, name="coupon_list"),
    path("edit_coupon/<int:pk>/", views.edit_coupon, name="edit_coupon"),
    path("add_coupon/", views.CouponCreateView.as_view(), name="add_coupon"),
    path(
        "delete_coupon/<int:pk>/",
        views.CouponDeleteView.as_view(),
        name="delete_coupon",
    ),
    path("activate_coupon/<int:pk>/", views.activate_coupon, name="activate_coupon"),
]
