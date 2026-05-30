from odoo import api, fields, models


class FitnessTrainer(models.Model):
    """Trainer who conducts fitness classes.

    Optionally linked to a system user (``res.users``) so that the
    trainer can log in and see only their own classes via record rules.
    """

    _name = 'fitness.trainer'
    _description = 'Fitness Club Trainer'
    _order = 'name'

    name = fields.Char(string='Full Name', required=True)

    specialization = fields.Char(
        string='Specialization',
        translate=True,
        help='Main discipline of the trainer (yoga, crossfit, ...).',
    )

    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')

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
        string='Classes',
        compute='_compute_class_count',
    )

    @api.depends('class_ids')
    def _compute_class_count(self):
        """Count classes assigned to this trainer (any state)."""
        for rec in self:
            rec.class_count = len(rec.class_ids)
