from datetime import date

from odoo import api, fields, models


class FitnessMember(models.Model):
    """Fitness club client.

    Linked to a standard ``res.partner`` for contact data. The model
    aggregates the client's subscriptions and attendances and exposes
    a computed ``subscription_state`` (active / expired / none).
    """

    _name = 'fitness.member'
    _description = 'Fitness Club Member'
    _order = 'name'

    partner_id = fields.Many2one(
        'res.partner',
        string='Full Name',
        required=True,
        ondelete='restrict',
        help='Standard partner used as a contact record for the member.',
    )
    
    name = fields.Char(
        string='Full Name',
        related='partner_id.name',
        store=True,
        readonly=False,
    )

    birthday = fields.Date(string='Date of Birth')
    
    age = fields.Integer(
        string='Age',
        compute='_compute_age',
        store=False,
    )

    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female')],
        string='Gender',
    )

    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
    email = fields.Char(related='partner_id.email', store=True, readonly=False)
    active = fields.Boolean(default=True)

    subscription_ids = fields.One2many(
        'fitness.subscription', 'member_id', string='Subscriptions',
    )

    active_subscription_id = fields.Many2one(
        'fitness.subscription',
        string='Active subscription',
        compute='_compute_active_subscription',
        store=True,
    )

    subscription_state = fields.Selection(
        selection=[
            ('none', 'No subscription'),
            ('active', 'Active'),
            ('expired', 'Expired'),
        ],
        string='Subscription status',
        compute='_compute_active_subscription',
        store=True,
    )

    attendance_ids = fields.One2many(
        'fitness.attendance', 'member_id', string='Attendances',
    )

    attendance_count = fields.Integer(
        string='Attendances',
        compute='_compute_attendance_count',
    )

    @api.depends('birthday')
    def _compute_age(self):
        """Age in full years computed from ``birthday``."""
        today = date.today()
        for rec in self:
            if rec.birthday:
                bd = rec.birthday
                rec.age = today.year - bd.year - (
                    (today.month, today.day) < (bd.month, bd.day)
                )
            else:
                rec.age = 0

    @api.depends('subscription_ids', 'subscription_ids.state')
    def _compute_active_subscription(self):
        """Pick the most recent active subscription, otherwise expired/none."""
        for rec in self:
            active = rec.subscription_ids.filtered(
                lambda s: s.state == 'active'
            )
            if active:
                rec.active_subscription_id = active.sorted(
                    'date_end', reverse=True
                )[0]
                rec.subscription_state = 'active'
            elif rec.subscription_ids:
                rec.active_subscription_id = False
                rec.subscription_state = 'expired'
            else:
                rec.active_subscription_id = False
                rec.subscription_state = 'none'

    @api.depends('attendance_ids')
    def _compute_attendance_count(self):
        """Total number of attendance records for this member."""
        for rec in self:
            rec.attendance_count = len(rec.attendance_ids)
