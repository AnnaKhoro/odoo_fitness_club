from datetime import date, timedelta

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FitnessSubscription(models.Model):
    """Concrete subscription of a member to a plan.

    The end date is derived from ``date_start`` + ``plan.duration_days``.
    The state transitions automatically from ``active`` to ``expired``
    when the end date is reached.
    """

    _name = 'fitness.subscription'
    _description = 'Fitness Subscription'
    _order = 'date_start desc, id desc'

    name = fields.Char(
        string='Reference',
        compute='_compute_name',
        store=True,
    )

    member_id = fields.Many2one(
        'fitness.member',
        string='Member',
        required=True,
        ondelete='cascade',
    )

    plan_id = fields.Many2one(
        'fitness.plan', string='Plan', required=True,
    )

    date_start = fields.Date(
        string='Start date',
        required=True,
        default=fields.Date.context_today,
    )
    date_end = fields.Date(
        string='End date',
        compute='_compute_date_end',
        store=True,
    )

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        compute='_compute_state',
        store=True,
    )

    manual_state = fields.Selection(
        selection=[('cancelled', 'Cancelled')],
        string='Manual override',
        help='Set to "cancelled" to mark this subscription as cancelled.',
    )

    days_left = fields.Integer(
        string='Days left',
        compute='_compute_days_left',
    )

    visits_used = fields.Integer(
        string='Visits used',
        compute='_compute_visits_used',
    )

    price = fields.Float(related='plan_id.price', store=True)

    @api.depends('member_id', 'plan_id', 'date_start')
    def _compute_name(self):
        """Human-readable reference: ``<member> - <plan> (<start>)``."""
        for rec in self:
            parts = [
                rec.member_id.name or '',
                rec.plan_id.name or '',
            ]
            if rec.date_start:
                parts.append(str(rec.date_start))
            rec.name = ' - '.join(p for p in parts if p)

    @api.depends('date_start', 'plan_id', 'plan_id.duration_days')
    def _compute_date_end(self):
        """End date = start + plan duration days."""
        for rec in self:
            if rec.date_start and rec.plan_id:
                rec.date_end = rec.date_start + timedelta(
                    days=rec.plan_id.duration_days
                )
            else:
                rec.date_end = False

    @api.depends('date_start', 'date_end', 'manual_state')
    def _compute_state(self):
        """Derive subscription state from dates and manual override."""
        today = date.today()
        for rec in self:
            if rec.manual_state == 'cancelled':
                rec.state = 'cancelled'
            elif not rec.date_start or not rec.date_end:
                rec.state = 'draft'
            elif rec.date_end < today:
                rec.state = 'expired'
            elif rec.date_start <= today:
                rec.state = 'active'
            else:
                rec.state = 'draft'

    @api.depends('date_end')
    def _compute_days_left(self):
        """Days remaining until expiration; 0 if already expired."""
        today = date.today()
        for rec in self:
            if rec.date_end and rec.date_end >= today:
                rec.days_left = (rec.date_end - today).days
            else:
                rec.days_left = 0

    @api.depends('member_id', 'date_start', 'date_end')
    def _compute_visits_used(self):
        """Count attendances of the member that fall inside the period."""
        Attendance = self.env['fitness.attendance']
        for rec in self:
            if not rec.member_id or not rec.date_start:
                rec.visits_used = 0
                continue
            domain = [
                ('member_id', '=', rec.member_id.id),
                ('attended_on', '>=', rec.date_start),
            ]
            if rec.date_end:
                domain.append(('attended_on', '<=', rec.date_end))
            rec.visits_used = Attendance.search_count(domain)

    @api.constrains('date_start')
    def _check_date_start_not_too_old(self):
        """Disallow back-dating a subscription more than 30 days."""
        limit = date.today() - timedelta(days=30)
        for rec in self:
            if rec.date_start and rec.date_start < limit:
                raise ValidationError(
                    'Start date cannot be more than 30 days in the past.'
                )

    def action_cancel(self):
        """Mark subscription as cancelled (manual override)."""
        self.write({'manual_state': 'cancelled'})
