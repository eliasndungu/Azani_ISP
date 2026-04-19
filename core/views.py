"""Views for dashboard, institutions, payments, and reports."""

from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import InstitutionForm
from .models import Infrastructure, Institution, Payment


class DashboardView(TemplateView):
    """Display high-level summary counts for institutions and payments."""

    template_name = 'core/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['institution_count'] = Institution.objects.count()
        context['overdue_payments_count'] = Payment.objects.filter(
            status=Payment.PaymentStatus.OVERDUE
        ).count()
        context['disconnected_count'] = Institution.objects.filter(
            status=Institution.InstitutionStatus.DISCONNECTED
        ).count()
        return context


class InstitutionListView(ListView):
    """List all registered institutions."""

    model = Institution
    template_name = 'core/institutions/list.html'
    context_object_name = 'institutions'


class InstitutionDetailView(DetailView):
    """Show details for a specific institution."""

    model = Institution
    template_name = 'core/institutions/detail.html'
    context_object_name = 'institution'


class InstitutionCreateView(CreateView):
    """Register a new institution in the system."""

    form_class = InstitutionForm
    template_name = 'core/institutions/form.html'
    success_url = reverse_lazy('core:institutions-list')


class PaymentListView(ListView):
    """List all institution payment records."""

    model = Payment
    template_name = 'core/payments/list.html'
    context_object_name = 'payments'


class DefaultersReportView(ListView):
    """List institutions that have overdue payments."""

    model = Institution
    template_name = 'core/reports/defaulters.html'
    context_object_name = 'institutions'

    def get_queryset(self):
        return Institution.objects.filter(payments__status=Payment.PaymentStatus.OVERDUE).distinct()


class DisconnectedReportView(ListView):
    """List all disconnected institutions."""

    model = Institution
    template_name = 'core/reports/disconnected.html'
    context_object_name = 'institutions'

    def get_queryset(self):
        return Institution.objects.filter(status=Institution.InstitutionStatus.DISCONNECTED)


class InfrastructureReportView(ListView):
    """List infrastructure records for all institutions."""

    model = Infrastructure
    template_name = 'core/reports/infrastructure.html'
    context_object_name = 'infrastructures'

    def get_queryset(self):
        return Infrastructure.objects.select_related('institution').all()
