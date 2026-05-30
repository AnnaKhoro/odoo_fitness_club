from odoo import fields, models


class ResUsers(models.Model):
    """Extend ``res.users`` with a link to a fitness trainer record.

    Lets the system identify which Odoo user corresponds to which
    trainer (used later for record rules: "show me only my classes").
    """

    _inherit = 'res.users'

    fitness_trainer_id = fields.Many2one(
        'fitness.trainer',
        string='Fitness trainer',
        help='Trainer profile linked to this system user.',
    )
