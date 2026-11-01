from timeit import default_timer

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from .models import Product, Order, ProductImage
from .forms import ProductForm, OrderForm

class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        categories = [
            "Laptops",
            "Smartphones",
            "Watches", "Desktops",
            "Notebooks",
            "Other products"
        ]

        context = {
            "time_running": default_timer(),
            "categories": categories,
        }

        return render(
            request, "shopapp/index.html", context=context
        )


class ProductListView(ListView):
    template_name = "shopapp/product_list.html"
    queryset = Product.objects.filter(on_store=True)
    context_object_name = "products"


class ProductDetailsView(DetailView):
    model = Product
    context_object_name = "product"


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy("shopapp:product_list")

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist("images")

        for image in images:
            ProductImage.objects.create(
                product=self.object,
                image=image
            )

        return response


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name_suffix = "_update_form"
    context_object_name = "product"

    def get_success_url(self):
        return reverse(
            "shopapp:product_detail",
            kwargs={"pk": self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        images = self.request.FILES.getlist("images")

        for image in images:
            ProductImage.objects.create(
                product=self.object,
                image=image
            )

        return response


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:product_list")
    context_object_name = "product"

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.on_store = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class OrderListView(ListView):
    context_object_name = "orders"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderDetailView(DetailView):
    context_object_name = "order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("shopapp:order_list")


class OrderUpdateView(UpdateView):
    model = Order
    form_class = OrderForm
    template_name_suffix = "_update_form"
    context_object_name = "order"

    def get_success_url(self):
        return reverse(
            "shopapp:order_detail",
            kwargs={"pk": self.object.pk},
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:order_list")
    context_object_name = "order"