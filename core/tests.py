"""Focused tests for core computations and routing scaffolds."""

from datetime import date
from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from .computations import (
    INSTALLATION_FEE,
    RECONNECTION_FEE,
    calculate_installation_cost,
    calculate_monthly_charge_with_upgrade,
    calculate_overdue_fine,
    calculate_total_charges,
    get_lan_cost,
)
from .models import BandwidthPlan, Fine, Infrastructure, Institution, LANPricing, Payment, Subscription


class ComputationTests(TestCase):
    def setUp(self):
        self.institution = Institution.objects.create(
            name='Azani Junior',
            type=Institution.InstitutionType.JUNIOR,
            address='Nairobi',
        )
        LANPricing.objects.create(min_nodes=2, max_nodes=10, cost=Decimal('10000.00'))
        self.plan = BandwidthPlan.objects.create(bandwidth_mbps=10, cost_per_month=Decimal('2000.00'))

    def test_get_lan_cost_from_pricing_range(self):
        self.assertEqual(get_lan_cost(5), Decimal('10000.00'))

    def test_calculate_installation_cost_includes_pc_and_lan(self):
        Infrastructure.objects.create(
            institution=self.institution,
            num_computers=2,
            num_lan_nodes=5,
            is_ready=True,
        )
        self.assertEqual(calculate_installation_cost(self.institution), INSTALLATION_FEE + Decimal('90000.00'))

    def test_calculate_monthly_charge_with_upgrade_applies_discount(self):
        subscription = Subscription.objects.create(
            institution=self.institution,
            plan=self.plan,
            start_date=date.today(),
            is_upgraded=True,
        )
        self.assertEqual(calculate_monthly_charge_with_upgrade(subscription), Decimal('1800.0000'))

    def test_calculate_total_charges_combines_monthly_overdue_and_reconnection(self):
        payment = Payment.objects.create(
            institution=self.institution,
            payment_type=Payment.PaymentType.MONTHLY,
            amount=Decimal('2000.00'),
            due_date=date.today(),
            status=Payment.PaymentStatus.OVERDUE,
        )
        Fine.objects.create(
            institution=self.institution,
            payment=payment,
            fine_type=Fine.FineType.RECONNECTION,
            fine_amount=RECONNECTION_FEE,
        )
        self.assertEqual(calculate_overdue_fine(payment), Decimal('300.0000'))
        self.assertEqual(calculate_total_charges(self.institution), Decimal('3300.0000'))


class RouteSmokeTests(TestCase):
    def test_dashboard_renders(self):
        response = self.client.get(reverse('core:dashboard'))
        self.assertEqual(response.status_code, 200)
