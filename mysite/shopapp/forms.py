from django import forms

from .models import Product, Order


class CSVImportForm(forms.Form):
    csv_file = forms.FileField()


class MultipleClearableFileInput(forms.ClearableFileInput):
    allow_multiple_accept = True

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["attrs"]["multiple"] = True
        return context


class ProductForm(forms.ModelForm):
    images = forms.ImageField(
        widget=MultipleClearableFileInput(),
        required=False,
        label="Additional images"
    )

    class Meta:
        model = Product
        fields = (
            "name", "price", "description", "discount", "preview",
        )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promo_code", "user", "products"