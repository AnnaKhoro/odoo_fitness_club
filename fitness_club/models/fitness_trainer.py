from odoo import api, fields, models


class FitnessTrainer(models.Model):
    """Trainer who conducts fitness classes.

    Optionally linked to a system user (``res.users``) so that the
    trainer can log in and see only their own classes via record rules.
    """

    _name = 'fitness.trainer'
    _description = 'Fitness Club Trainer'
    _order = 'name'

    partner_id = fields.Many2one(
        'res.partner',
        string='Full Name',
        required=True,
        ondelete='restrict',
        help='Standard partner used as a contact record for the trainer.',
    )
    
    name = fields.Char(
        related='partner_id.name',
        store=True,
        readonly=False,
    )

    specialization = fields.Char(
        string='Specialization',
        translate=True,
        help='Main discipline of the trainer (yoga, crossfit, ...).',
    )

    phone = fields.Char(related='partner_id.phone', store=True, readonly=False)
    email = fields.Char(related='partner_id.email', store=True, readonly=False)

    user_id = fields.Many2one(
        'res.users',
        string='System User',
        help='If set, the trainer can log in with this user account.',
    )

    active = fields.Boolean(default=True)

    class_ids = fields.One2many(
        'fitness.class', 'trainer_id', string='Classes',
    )

    class_count = fields.Integer(
        string='Classes count',
        compute='_compute_class_count',
    )

    @api.depends('class_ids')
    def _compute_class_count(self):
        """Count classes assigned to this trainer (any state)."""
        for rec in self:
            rec.class_count = len(rec.class_ids)
