from odoo import fields, models


class FitnessPlan(models.Model):
    """Subscription plan offered by the fitness club.

    A plan defines the duration (in days), price and (optional) visit
    cap. Concrete client subscriptions reference a plan to derive their
    expiry date and pricing.
    """

    _name = 'fitness.plan'
    _description = 'Fitness Subscription Plan'
    _order = 'sequence, name'

    name = fields.Char(
        string='Name',
        required=True,
        translate=True,
        help='Display name of the plan, e.g. "Monthly", "Yearly", '
             '"10 visits".',
    )

    sequence = fields.Integer(default=10)

    duration_days = fields.Integer(
        string='Duration (days)',
        required=True,
        default=30,
        help='How many days the subscription lasts from its start date.',
    )

    price = fields.Float(string='Price', required=True, default=0.0)

    max_visits = fields.Integer(
        string='Max visits',
        default=0,
        help='Maximum number of visits allowed. 0 = unlimited.',
    )

    description = fields.Text(string='Description', translate=True)
    active = fields.Boolean(default=True)
