"""URL routes for core Azani ISP views."""

from django.urls import path

from .views import (
    DashboardView,
    DefaultersReportView,
    DisconnectedReportView,
    InfrastructureReportView,
    InstitutionCreateView,
    InstitutionDetailView,
    InstitutionListView,
    PaymentListView,
)

app_name = 'core'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('institutions/', InstitutionListView.as_view(), name='institutions-list'),
    path('institutions/<int:pk>/', InstitutionDetailView.as_view(), name='institutions-detail'),
    path('institutions/add/', InstitutionCreateView.as_view(), name='institutions-add'),
    path('payments/', PaymentListView.as_view(), name='payments-list'),
    path('reports/defaulters/', DefaultersReportView.as_view(), name='reports-defaulters'),
    path('reports/disconnected/', DisconnectedReportView.as_view(), name='reports-disconnected'),
    path('reports/infrastructure/', InfrastructureReportView.as_view(), name='reports-infrastructure'),
]
