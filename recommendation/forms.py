from django import forms
from .models import Booking, ProfessionalHouseboatDataset500Rows


# ======================================================
# Booking Form
# ======================================================

class BookingForm(forms.ModelForm):

    class Meta:
        model = Booking

        fields = [
            "customer_name",
            "email",
            "phone",
            "checkin",
            "checkout",
            "guests",
        ]

        widgets = {
            "checkin": forms.DateInput(attrs={"type": "date"}),
            "checkout": forms.DateInput(attrs={"type": "date"}),
        }


# ======================================================
# Houseboat Form
# ======================================================

class HouseboatForm(forms.ModelForm):

    class Meta:
        model = ProfessionalHouseboatDataset500Rows

        fields = [
            "houseboatname",
            "location",
            "priceinr",
            "rating",
            "capacity",
            "bedrooms",
            "ac",
            "wifi",
            "imagefile",
        ]