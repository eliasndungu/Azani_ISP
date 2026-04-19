"""Data models for the Azani ISP information system."""

from django.db import models


class Institution(models.Model):
    """Represents a school or college that subscribes to Azani ISP services."""

    class InstitutionType(models.TextChoices):
        PRIMARY = 'primary', 'Primary'
        JUNIOR = 'junior', 'Junior'
        SENIOR = 'senior', 'Senior'
        COLLEGE = 'college', 'College'

    class InstitutionStatus(models.TextChoices):
        ACTIVE = 'active', 'Active'
        DISCONNECTED = 'disconnected', 'Disconnected'

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=InstitutionType.choices)
    address = models.TextField()
    registration_date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=InstitutionStatus.choices,
        default=InstitutionStatus.ACTIVE,
    )

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    def __str__(self):
        return self.name


class ContactPerson(models.Model):
    """Stores the designated contact person for an institution."""

    institution = models.OneToOneField(
        Institution,
        on_delete=models.CASCADE,
        related_name='contact_person',
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    class Meta:
        verbose_name = 'Contact Person'
        verbose_name_plural = 'Contact Persons'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.institution.name})'


class BandwidthPlan(models.Model):
    """Defines available monthly bandwidth plans and their prices."""

    class BandwidthChoices(models.IntegerChoices):
        MBPS_4 = 4, '4 Mbps'
        MBPS_10 = 10, '10 Mbps'
        MBPS_20 = 20, '20 Mbps'
        MBPS_25 = 25, '25 Mbps'
        MBPS_50 = 50, '50 Mbps'

    bandwidth_mbps = models.IntegerField(choices=BandwidthChoices.choices, unique=True)
    cost_per_month = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Bandwidth Plan'
        verbose_name_plural = 'Bandwidth Plans'

    def __str__(self):
        return f'{self.bandwidth_mbps} Mbps - KSh {self.cost_per_month}'


class Subscription(models.Model):
    """Tracks an institution's subscribed bandwidth plan and upgrade history."""

    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    plan = models.ForeignKey(BandwidthPlan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    is_upgraded = models.BooleanField(default=False)
    previous_plan = models.ForeignKey(
        BandwidthPlan,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='upgrades_from',
    )

    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'

    def __str__(self):
        return f'{self.institution.name} - {self.plan.bandwidth_mbps} Mbps'


class Payment(models.Model):
    """Captures registration, installation, and monthly payments for institutions."""

    class PaymentType(models.TextChoices):
        REGISTRATION = 'registration', 'Registration'
        INSTALLATION = 'installation', 'Installation'
        MONTHLY = 'monthly', 'Monthly'

    class PaymentStatus(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'
        OVERDUE = 'overdue', 'Overdue'

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.CharField(max_length=20, choices=PaymentType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateField(null=True, blank=True)
    due_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
    )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        return f'{self.institution.name} - {self.payment_type} ({self.status})'


class Infrastructure(models.Model):
    """Represents ICT and LAN infrastructure details for an institution."""

    institution = models.OneToOneField(
        Institution,
        on_delete=models.CASCADE,
        related_name='infrastructure',
    )
    num_computers = models.IntegerField(default=0)
    num_lan_nodes = models.IntegerField(default=0)
    is_ready = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Infrastructure'
        verbose_name_plural = 'Infrastructure'

    def __str__(self):
        return f'{self.institution.name} Infrastructure'


class Fine(models.Model):
    """Stores fines charged to institutions for overdue and reconnection events."""

    class FineType(models.TextChoices):
        OVERDUE = 'overdue', 'Overdue'
        RECONNECTION = 'reconnection', 'Reconnection'

    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, related_name='fines')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='fines')
    fine_type = models.CharField(max_length=20, choices=FineType.choices)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2)
    fine_date = models.DateField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Fine'
        verbose_name_plural = 'Fines'

    def __str__(self):
        return f'{self.institution.name} - {self.fine_type} fine'


class LANPricing(models.Model):
    """Pricing tiers used to calculate LAN setup cost based on node ranges."""

    min_nodes = models.IntegerField()
    max_nodes = models.IntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'LAN Pricing'
        verbose_name_plural = 'LAN Pricing'

    def __str__(self):
        return f'{self.min_nodes}-{self.max_nodes} nodes: KSh {self.cost}'
