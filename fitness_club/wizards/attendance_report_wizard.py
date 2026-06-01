from odoo import api, fields, models


class AttendanceReportWizard(models.TransientModel):
    """Wizard producing a filtered attendance list.

    Lets the user select a period and (optionally) specific members
    and/or trainers, then opens the matching ``fitness.attendance``
    records grouped by member.
    """

    _name = 'attendance.report.wizard'
    _description = 'Attendance report wizard'

    date_from = fields.Date(string='From')
    date_to = fields.Date(string='To')
    member_ids = fields.Many2many(
        'fitness.member',
        'attendance_report_wizard_member_rel',
        'wizard_id', 'member_id',
        string='Members',
    )
    trainer_ids = fields.Many2many(
        'fitness.trainer',
        'attendance_report_wizard_trainer_rel',
        'wizard_id', 'trainer_id',
        string='Trainers',
    )

    @api.model
    def default_get(self, fields_list):
        """Pre-fill members or trainers when launched from their list."""
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids') or []
        if active_model == 'fitness.member' and active_ids:
            res['member_ids'] = [(6, 0, active_ids)]
        elif active_model == 'fitness.trainer' and active_ids:
            res['trainer_ids'] = [(6, 0, active_ids)]
        return res

    def action_generate(self):
        """Return an action that opens the filtered attendance list."""
        self.ensure_one()
        domain = []
        if self.date_from:
            domain.append(('attended_on', '>=', self.date_from))
        if self.date_to:
            domain.append(('attended_on', '<=', self.date_to))
        if self.member_ids:
            domain.append(('member_id', 'in', self.member_ids.ids))
        if self.trainer_ids:
            domain.append(
                ('class_id.trainer_id', 'in', self.trainer_ids.ids)
            )
        return {
            'name': 'Attendances',
            'type': 'ir.actions.act_window',
            'res_model': 'fitness.attendance',
            'view_mode': 'list,form,pivot,graph',
            'domain': domain,
            'context': {'search_default_group_member': 1},
            'target': 'main',
        }
