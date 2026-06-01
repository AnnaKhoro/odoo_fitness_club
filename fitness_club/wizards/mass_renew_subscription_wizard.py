from odoo import fields, models


class MassRenewSubscriptionWizard(models.TransientModel):
    """Bulk-create new subscriptions for a set of fitness members.

    Called from the Members list view (Actions menu). For every
    selected member, a new ``fitness.subscription`` is created with the
    chosen plan and start date.
    """

    _name = 'mass.renew.subscription.wizard'
    _description = 'Mass renew subscription'

    plan_id = fields.Many2one(
        'fitness.plan', string='Plan', required=True,
    )
    date_start = fields.Date(
        string='Start date',
        default=fields.Date.context_today,
        required=True,
    )

    def action_apply(self):
        """Create new subscriptions for all selected members."""
        self.ensure_one()
        member_ids = self.env.context.get('active_ids') or []
        if not member_ids:
            return {'type': 'ir.actions.act_window_close'}
        members = self.env['fitness.member'].browse(member_ids)
        Subscription = self.env['fitness.subscription']
        for member in members:
            Subscription.create({
                'member_id': member.id,
                'plan_id': self.plan_id.id,
                'date_start': self.date_start,
            })
        return {'type': 'ir.actions.act_window_close'}
