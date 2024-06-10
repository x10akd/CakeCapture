from django.urls import path
from . import views

app_name = "managements"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add_product/", views.ProductCreateView.as_view(), name="add_product"),
    path("edit_product/<int:pk>/", views.edit_product, name="edit_product"),
    path("delete_product/<int:pk>/", views.delete_product, name="delete_product"),
    path("category_list/", views.category_list, name="category_list"),
    path("add_category/", views.CategoryCreateView.as_view(), name="add_category"),
    path("edit_category/<int:pk>/", views.edit_category, name="edit_category"),
    path("delete_category/<int:pk>/", views.delete_category, name="delete_category"),
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
    path("order_list/", views.order_list, name="order_list"),
    path("feedback_list/", views.feedback_list, name="feedback_list"),
    path("feedback_reply/<int:pk>/", views.feedback_reply, name="feedback_reply"),
    path("favorite_charts/", views.favorite_charts, name="favorite_charts"),
    path(
        "month_sell_quantity_charts/",
        views.month_sell_quantity_charts,
        name="month_sell_quantity_charts",
    ),
    path(
        "month_sell_amount_charts/",
        views.month_sell_amount_charts,
        name="month_sell_amount_charts",
    ),
]
