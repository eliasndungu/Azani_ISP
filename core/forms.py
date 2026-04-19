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
        fields = ['name', 'type', 'address', 'status']


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = ['institution', 'first_name', 'last_name', 'phone', 'email']


class BandwidthPlanForm(forms.ModelForm):
    class Meta:
        model = BandwidthPlan
        fields = ['bandwidth_mbps', 'cost_per_month']


class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['institution', 'plan', 'start_date', 'is_upgraded', 'previous_plan']


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['institution', 'payment_type', 'amount', 'payment_date', 'due_date', 'status']


class InfrastructureForm(forms.ModelForm):
    class Meta:
        model = Infrastructure
        fields = ['institution', 'num_computers', 'num_lan_nodes', 'is_ready']


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ['institution', 'payment', 'fine_type', 'fine_amount', 'is_paid']


class LANPricingForm(forms.ModelForm):
    class Meta:
        model = LANPricing
        fields = ['min_nodes', 'max_nodes', 'cost']
