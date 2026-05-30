from odoo import api, fields, models


class ResPartner(models.Model):
    """Extend ``res.partner`` with fitness-club related metadata."""

    _inherit = 'res.partner'

    fitness_member_ids = fields.One2many(
        'fitness.member', 'partner_id', string='Fitness memberships',
    )
    is_fitness_member = fields.Boolean(
        string='Is fitness member',
        compute='_compute_is_fitness_member',
        store=True,
    )

    @api.depends('fitness_member_ids')
    def _compute_is_fitness_member(self):
        """True when the partner has at least one club membership."""
        for rec in self:
            rec.is_fitness_member = bool(rec.fitness_member_ids)
