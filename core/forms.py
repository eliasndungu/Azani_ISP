"""Model forms for Azani ISP entities."""

from django import forms

from .models import (
    BandwidthPlan,
    ContactPerson,
    Fine,
    Infrastructure,
    Institution,
    LANPricing,
    Payment,
    Subscription,
)


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = '__all__'


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = '__all__'


class BandwidthPlanForm(forms.ModelForm):
    class Meta:
        model = BandwidthPlan
        fields = '__all__'


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = '__all__'


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'


class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = '__all__'


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = '__all__'


class LANPricingForm(forms.ModelForm):
    class Meta:
        model = LANPricing
        fields = '__all__'
