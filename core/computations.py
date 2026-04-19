"""Business computation functions for the Azani ISP information system."""

from decimal import Decimal

from .models import Fine, Infrastructure, LANPricing, Payment

REGISTRATION_FEE = Decimal('8500')
INSTALLATION_FEE = Decimal('10000')
PC_COST = Decimal('40000')
OVERDUE_FINE_RATE = Decimal('0.15')  # 15%
UPGRADE_DISCOUNT = Decimal('0.10')  # 10%
RECONNECTION_FEE = Decimal('1000')


def get_lan_cost(num_nodes):
    """Return LAN setup cost for a node count based on configured LANPricing tiers.

    Parameters:
        num_nodes (int): Number of LAN nodes required by the institution.

    Returns:
        Decimal: Matching LAN tier cost. Returns Decimal('0.00') when no tier matches
        the provided node count or when the value is less than 1.

    Business rules:
        - LAN cost is sourced from the LANPricing table.
        - A tier is selected when min_nodes <= num_nodes <= max_nodes.
    """

    if num_nodes < 1:
        return Decimal('0.00')

    pricing = LANPricing.objects.filter(min_nodes__lte=num_nodes, max_nodes__gte=num_nodes).first()
    return pricing.cost if pricing else Decimal('0.00')


def calculate_pc_and_lan_cost(institution):
    """Compute hardware provisioning cost for an institution.

    Parameters:
        institution (Institution): Institution whose infrastructure costs are being computed.

    Returns:
        Decimal: Total cost of computers and LAN for the institution. Returns
        Decimal('0.00') when no infrastructure record exists.

    Business rules:
        - Each required computer costs KSh 40,000.
        - LAN cost is determined using LANPricing ranges via get_lan_cost.
    """

    try:
        infrastructure = institution.infrastructure
    except Infrastructure.DoesNotExist:
        return Decimal('0.00')

    pc_cost = Decimal(infrastructure.num_computers) * PC_COST
    lan_cost = get_lan_cost(infrastructure.num_lan_nodes)
    return pc_cost + lan_cost


def calculate_installation_cost(institution):
    """Compute total installation charge for an institution.

    Parameters:
        institution (Institution): Institution being installed.

    Returns:
        Decimal: Total installation charge as installation fee + PCs and LAN cost.

    Business rules:
        - Base installation fee is KSh 10,000.
        - Additional infrastructure costs are included using calculate_pc_and_lan_cost.
    """

    return INSTALLATION_FEE + calculate_pc_and_lan_cost(institution)


def calculate_monthly_charge_with_upgrade(subscription):
    """Calculate monthly subscription charge after considering upgrade discount.

    Parameters:
        subscription (Subscription): Subscription instance with current plan details.

    Returns:
        Decimal: Monthly plan cost, discounted by 10% only when is_upgraded is True.

    Business rules:
        - Upgraded plans get a 10% discount.
        - Non-upgraded plans are billed at full plan cost.
    """

    plan_cost = subscription.plan.cost_per_month
    if subscription.is_upgraded:
        return plan_cost * (Decimal('1.00') - UPGRADE_DISCOUNT)
    return plan_cost


def calculate_overdue_fine(payment):
    """Calculate overdue fine for a specific payment.

    Parameters:
        payment (Payment): Payment that is overdue.

    Returns:
        Decimal: Fine amount equal to 15% of the payment amount.

    Business rules:
        - Overdue fine is always 15% of amount due.
    """

    return payment.amount * OVERDUE_FINE_RATE


def calculate_total_charges(institution):
    """Calculate total charges owed by an institution.

    Parameters:
        institution (Institution): Institution whose total charges are aggregated.

    Returns:
        Decimal: Total amount composed of monthly charges, overdue fines, and
        reconnection fees.

    Business rules:
        - Monthly charges come from Payment records with payment_type='monthly'.
        - Overdue fines are computed at 15% for overdue payments.
        - Reconnection fees are KSh 1,000 per reconnection fine record.
    """

    monthly_total = (
        institution.payments.filter(payment_type=Payment.PaymentType.MONTHLY)
        .values_list('amount', flat=True)
    )
    monthly_charges = sum(monthly_total, Decimal('0.00'))

    overdue_payments = institution.payments.filter(status=Payment.PaymentStatus.OVERDUE)
    overdue_fines = sum((calculate_overdue_fine(payment) for payment in overdue_payments), Decimal('0.00'))

    reconnection_count = institution.fines.filter(fine_type=Fine.FineType.RECONNECTION).count()
    reconnection_fees = RECONNECTION_FEE * Decimal(reconnection_count)

    return monthly_charges + overdue_fines + reconnection_fees


def get_aggregate_per_service(institution):
    """Return service-level financial aggregates for one institution.

    Parameters:
        institution (Institution): Institution to summarize.

    Returns:
        dict[str, Decimal]: A dictionary with registration, installation, monthly,
        overdue fine, reconnection fee, and total aggregates.

    Business rules:
        - Payment totals are grouped by payment type.
        - Overdue fine totals are derived from overdue payments at 15% each.
        - Reconnection totals are computed as count(reconnection fines) × KSh 1,000.
    """

    registration_total = sum(
        institution.payments.filter(payment_type=Payment.PaymentType.REGISTRATION).values_list('amount', flat=True),
        Decimal('0.00'),
    )
    installation_total = sum(
        institution.payments.filter(payment_type=Payment.PaymentType.INSTALLATION).values_list('amount', flat=True),
        Decimal('0.00'),
    )
    monthly_total = sum(
        institution.payments.filter(payment_type=Payment.PaymentType.MONTHLY).values_list('amount', flat=True),
        Decimal('0.00'),
    )
    overdue_total = sum(
        (
            calculate_overdue_fine(payment)
            for payment in institution.payments.filter(status=Payment.PaymentStatus.OVERDUE)
        ),
        Decimal('0.00'),
    )
    reconnection_total = RECONNECTION_FEE * Decimal(
        institution.fines.filter(fine_type=Fine.FineType.RECONNECTION).count()
    )

    return {
        'registration': registration_total,
        'installation': installation_total,
        'monthly': monthly_total,
        'overdue_fines': overdue_total,
        'reconnection_fees': reconnection_total,
        'total': registration_total + installation_total + monthly_total + overdue_total + reconnection_total,
    }
