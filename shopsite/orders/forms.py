from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "contact", "note", "payment_method", "address", "city", "postal_code"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "e.g. Maria Santos", "class": "pill-input", "required": True}),
            "contact": forms.TextInput(attrs={"placeholder": "GCash number, IG, or FB name", "class": "pill-input", "required": True}),
            "note": forms.Textarea(attrs={"placeholder": "Gift wrap, pickup, shade of mint...", "class": "pill-input pill-textarea", "rows": 2}),
            "payment_method": forms.HiddenInput(),
            "address": forms.HiddenInput(attrs={"required": False}),
            "city": forms.HiddenInput(attrs={"required": False}),
            "postal_code": forms.HiddenInput(attrs={"required": False}),
        }
