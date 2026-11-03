from django import forms

from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "brand", "car", "price", "photo", "badge", "in_stock"]

class OrderForm(forms.Form):
    name = forms.CharField(label="Ваше имя", max_length=100)
    phone = forms.CharField(
        label="Телефон",
        max_length=30,
        widget=forms.TextInput(attrs={"type": "tel", "placeholder": "+996 700 00 00 00"}),
    )
    quantity = forms.IntegerField(label="Количество", min_value=1, max_value=99, initial=1)
    comment = forms.CharField(
        label="Комментарий",
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Марка, год авто, пожелания"}),
    )
