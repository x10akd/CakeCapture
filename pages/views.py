from django.shortcuts import render


def detail(req):
    return render(req, "item_detail/item_detail.html")
