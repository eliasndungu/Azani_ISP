# Azani ISP Information System

Azani ISP Information System is a Django + SQLite school project for managing institutions, subscriptions, payments, fines, and infrastructure for internet service delivery.

## Setup Instructions

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```bash
   python manage.py migrate
   ```
5. (Optional) Load initial fixture data:
   ```bash
   python manage.py loaddata core/fixtures/initial_data.json
   ```
6. Run the development server:
   ```bash
   python manage.py runserver
   ```

## Business Rules

- Registration fee: **KSh 8,500**
- Installation fee: **KSh 10,000**
- Computer cost: **KSh 40,000** per PC
- Overdue fine rate: **15%** of overdue amount
- Upgrade discount: **10%** on upgraded bandwidth plans
- Reconnection fee: **KSh 1,000**

### Bandwidth Plans

| Plan (Mbps) | Monthly Cost (KSh) |
|---|---:|
| 4 | 1,200 |
| 10 | 2,000 |
| 20 | 3,500 |
| 25 | 4,000 |
| 50 | 7,000 |

### LAN Pricing Tiers

| Node Range | Cost (KSh) |
|---|---:|
| 2-10 | 10,000 |
| 11-20 | 20,000 |
| 21-40 | 30,000 |
| 41-100 | 40,000 |

## Models Overview

| Model | Purpose |
|---|---|
| Institution | Registered school/college profile and status |
| ContactPerson | Primary contact for an institution |
| BandwidthPlan | Supported internet package options |
| Subscription | Institution plan assignment and upgrades |
| Payment | Registration, installation, and monthly transactions |
| Infrastructure | Computers, LAN nodes, and readiness tracking |
| Fine | Overdue and reconnection penalties |
| LANPricing | LAN node range pricing table |

## Available Reports

- Defaulters report (institutions with overdue payments)
- Disconnected institutions report
- Infrastructure report per institution
