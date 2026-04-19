"""Admin registrations and configurations for Azani ISP models."""

from django.contrib import admin

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


@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'registration_date')
    search_fields = ('name', 'address', 'type')
    list_filter = ('type', 'status', 'registration_date')


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'institution', 'phone', 'email')
    search_fields = ('first_name', 'last_name', 'email', 'phone', 'institution__name')
    list_filter = ('institution__type',)


@admin.register(BandwidthPlan)
class BandwidthPlanAdmin(admin.ModelAdmin):
    list_display = ('bandwidth_mbps', 'cost_per_month')
    search_fields = ('=bandwidth_mbps',)
    list_filter = ('bandwidth_mbps',)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('institution', 'plan', 'start_date', 'is_upgraded', 'previous_plan')
    search_fields = ('institution__name', '=plan__bandwidth_mbps')
    list_filter = ('is_upgraded', 'start_date', 'plan')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('institution', 'payment_type', 'amount', 'payment_date', 'due_date', 'status')
    search_fields = ('institution__name', 'payment_type', 'status')
    list_filter = ('payment_type', 'status', 'due_date', 'payment_date')


@admin.register(Infrastructure)
class InfrastructureAdmin(admin.ModelAdmin):
    list_display = ('institution', 'num_computers', 'num_lan_nodes', 'is_ready')
    search_fields = ('institution__name',)
    list_filter = ('is_ready',)


@admin.register(Fine)
class FineAdmin(admin.ModelAdmin):
    list_display = ('institution', 'payment', 'fine_type', 'fine_amount', 'fine_date', 'is_paid')
    search_fields = ('institution__name', 'payment__payment_type', 'fine_type')
    list_filter = ('fine_type', 'is_paid', 'fine_date')


@admin.register(LANPricing)
class LANPricingAdmin(admin.ModelAdmin):
    list_display = ('min_nodes', 'max_nodes', 'cost')
    search_fields = ('=min_nodes', '=max_nodes')
    list_filter = ('min_nodes', 'max_nodes')
