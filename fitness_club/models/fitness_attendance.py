from odoo import api, fields, models
from odoo.exceptions import ValidationError


class FitnessAttendance(models.Model):
    """Record of a member attending a fitness class.

    A member can attend a specific class only once. The attendance also
    links back to the active subscription of the member at the moment
    of the visit (for analytics).
    """

    _name = 'fitness.attendance'
    _description = 'Fitness Class Attendance'
    _order = 'attended_on desc'

    member_id = fields.Many2one(
        'fitness.member', string='Member',
        required=True, ondelete='cascade',
    )
    class_id = fields.Many2one(
        'fitness.class', string='Class',
        required=True, ondelete='cascade',
    )
    subscription_id = fields.Many2one(
        'fitness.subscription',
        string='Subscription',
        compute='_compute_subscription_id',
        store=True,
    )
    attended_on = fields.Datetime(
        string='Attended on',
        default=fields.Datetime.now,
        required=True,
    )

    _sql_constraints = [
        (
            'member_class_uniq',
            'unique(member_id, class_id)',
            'A member can attend the same class only once.',
        ),
    ]

    @api.depends('member_id', 'attended_on')
    def _compute_subscription_id(self):
        """Find the active subscription of the member at the visit time."""
        Sub = self.env['fitness.subscription']
        for rec in self:
            if not rec.member_id or not rec.attended_on:
                rec.subscription_id = False
                continue
            day = fields.Date.to_date(rec.attended_on)
            sub = Sub.search([
                ('member_id', '=', rec.member_id.id),
                ('date_start', '<=', day),
                ('date_end', '>=', day),
                ('state', 'in', ('active', 'expired')),
            ], order='date_start desc', limit=1)
            rec.subscription_id = sub.id if sub else False

    @api.constrains('member_id', 'class_id')
    def _check_member_has_active_subscription(self):
        """Block attendance if member has no active subscription."""
        for rec in self:
            if rec.member_id.subscription_state != 'active':
                raise ValidationError(
                    "Member '%s' has no active subscription." % rec.member_id.name
                )

    @api.constrains('class_id')
    def _check_class_not_full(self):
        """Block attendance when the class is already at capacity."""
        for rec in self:
            cls = rec.class_id
            if cls.max_participants <= 0:
                continue
            current = self.env['fitness.attendance'].search_count([
                ('class_id', '=', cls.id),
            ])
            if current > cls.max_participants:
                raise ValidationError(
                    "Class '%s' is already full (max %s participants)."
                    % (cls.name, cls.max_participants)
                )
