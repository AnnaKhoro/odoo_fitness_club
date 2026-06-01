from datetime import timedelta

from odoo import api, fields, models


class FitnessClass(models.Model):
    """Group fitness class (yoga session, crossfit, etc.).

    Has a fixed scheduled time, a maximum capacity and a list of
    attending members. Drives the ``calendar`` view of the module.
    """

    _name = 'fitness.class'
    _description = 'Fitness Class'
    _order = 'start_datetime desc'

    name = fields.Char(string='Title', required=True, translate=True)
    trainer_id = fields.Many2one(
        'fitness.trainer', string='Trainer', required=True,
    )
    
    start_datetime = fields.Datetime(
        string='Starts at',
        required=True,
        default=fields.Datetime.now,
    )

    duration_min = fields.Integer(
        string='Duration (min)', default=60,
    )

    end_datetime = fields.Datetime(
        string='Ends at',
        compute='_compute_end_datetime',
        store=True,
    )

    max_participants = fields.Integer(
        string='Max participants', default=15,
    )
    
    state = fields.Selection(
        selection=[
            ('planned', 'Planned'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        compute='_compute_state',
        store=True,
    )

    manual_state = fields.Selection(
        selection=[('cancelled', 'Cancelled')],
        string='Manual override',
        help='Set to "cancelled" to force the class status to cancelled.',
    )

    notes = fields.Text(string='Notes')
    active = fields.Boolean(default=True)

    attendance_ids = fields.One2many(
        'fitness.attendance', 'class_id', string='Participants',
    )

    participant_count = fields.Integer(
        string='Participants count',
        compute='_compute_participant_count',
    )

    is_full = fields.Boolean(
        string='Is full',
        compute='_compute_participant_count',
    )

    @api.depends('start_datetime', 'duration_min')
    def _compute_end_datetime(self):
        """End time = start + duration."""
        for rec in self:
            if rec.start_datetime and rec.duration_min:
                rec.end_datetime = rec.start_datetime + timedelta(
                    minutes=rec.duration_min
                )
            else:
                rec.end_datetime = rec.start_datetime

    @api.depends('start_datetime', 'end_datetime', 'manual_state')
    def _compute_state(self):
        """Derive status from time + manual override.

        * ``cancelled`` — if manually cancelled.
        * ``done``      — if the class has already finished.
        * ``planned``   — otherwise.
        """
        now = fields.Datetime.now()
        for rec in self:
            if rec.manual_state == 'cancelled':
                rec.state = 'cancelled'
            elif rec.end_datetime and rec.end_datetime < now:
                rec.state = 'done'
            else:
                rec.state = 'planned'

    def action_cancel(self):
        """Manually mark the class as cancelled."""
        self.write({'manual_state': 'cancelled'})

    def action_reset(self):
        """Clear the manual cancellation so status falls back to auto."""
        self.write({'manual_state': False})

    @api.depends('attendance_ids', 'max_participants')
    def _compute_participant_count(self):
        """Count attendees and flag the class as full when applicable."""
        for rec in self:
            count = len(rec.attendance_ids)
            rec.participant_count = count
            rec.is_full = (
                rec.max_participants > 0
                and count >= rec.max_participants
            )
