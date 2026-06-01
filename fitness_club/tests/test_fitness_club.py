from datetime import date, datetime, timedelta

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestFitnessClub(TransactionCase):
    """Cover key behaviors of every fitness_club model."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Plan = cls.env['fitness.plan']
        cls.Trainer = cls.env['fitness.trainer']
        cls.Member = cls.env['fitness.member']
        cls.Subscription = cls.env['fitness.subscription']
        cls.Class = cls.env['fitness.class']
        cls.Attendance = cls.env['fitness.attendance']
        cls.Partner = cls.env['res.partner']

        cls.partner_a = cls.Partner.create({'name': 'Test Partner A'})
        cls.partner_b = cls.Partner.create({'name': 'Test Partner B'})
        cls.partner_trainer = cls.Partner.create({'name': 'Test Trainer'})

        cls.plan_monthly = cls.Plan.create({
            'name': 'Test Monthly',
            'duration_days': 30,
            'price': 50.0,
        })

        cls.trainer = cls.Trainer.create({
            'partner_id': cls.partner_trainer.id,
            'specialization': 'Yoga',
        })

        cls.member = cls.Member.create({
            'partner_id': cls.partner_a.id,
            'birthday': date(1990, 1, 1),
            'gender': 'male',
        })

    # 1. fitness.plan
    def test_plan_create(self):
        """Plan stores name, duration and price."""
        plan = self.Plan.create({
            'name': 'Test Plan',
            'duration_days': 14,
            'price': 25.0,
        })
        self.assertEqual(plan.name, 'Test Plan')
        self.assertEqual(plan.duration_days, 14)
        self.assertEqual(plan.price, 25.0)
        self.assertTrue(plan.active)

    # 2. fitness.member
    def test_member_age_and_name(self):
        """Age is computed from birthday and name comes from partner."""
        today = date.today()
        expected_age = today.year - 1990 - (
            (today.month, today.day) < (1, 1)
        )
        self.assertEqual(self.member.age, expected_age)
        self.assertEqual(self.member.name, self.partner_a.name)

    # 3. fitness.trainer
    def test_trainer_class_count(self):
        """class_count reflects the number of related classes."""
        self.assertEqual(self.trainer.class_count, 0)
        self.Class.create({
            'name': 'Test class',
            'trainer_id': self.trainer.id,
            'start_datetime': datetime.now() + timedelta(days=1),
            'duration_min': 60,
        })
        self.trainer.invalidate_recordset(['class_count'])
        self.assertEqual(self.trainer.class_count, 1)

    # 4. fitness.subscription
    def test_subscription_date_end_and_state(self):
        """date_end = date_start + plan.duration_days; state auto."""
        sub = self.Subscription.create({
            'member_id': self.member.id,
            'plan_id': self.plan_monthly.id,
            'date_start': date.today(),
        })
        self.assertEqual(
            sub.date_end, date.today() + timedelta(days=30)
        )
        self.assertEqual(sub.state, 'active')

    def test_subscription_old_start_rejected(self):
        """Subscription cannot be back-dated more than 30 days."""
        with self.assertRaises(ValidationError):
            self.Subscription.create({
                'member_id': self.member.id,
                'plan_id': self.plan_monthly.id,
                'date_start': date.today() - timedelta(days=60),
            })

    # 5. fitness.class
    def test_class_state_auto(self):
        """Class state is auto-computed from start/end datetime."""
        future = self.Class.create({
            'name': 'Future class',
            'trainer_id': self.trainer.id,
            'start_datetime': datetime.now() + timedelta(days=2),
            'duration_min': 60,
        })
        past = self.Class.create({
            'name': 'Past class',
            'trainer_id': self.trainer.id,
            'start_datetime': datetime.now() - timedelta(days=2),
            'duration_min': 60,
        })
        self.assertEqual(future.state, 'planned')
        self.assertEqual(past.state, 'done')

    def test_class_manual_cancel(self):
        """Manual override sets state to cancelled."""
        cls = self.Class.create({
            'name': 'To cancel',
            'trainer_id': self.trainer.id,
            'start_datetime': datetime.now() + timedelta(days=1),
        })
        cls.action_cancel()
        self.assertEqual(cls.state, 'cancelled')
        cls.action_reset()
        self.assertEqual(cls.state, 'planned')

    # 6. fitness.attendance
    def test_attendance_unique(self):
        """A member cannot attend the same class twice."""
        # active subscription required for attendance constraint to pass
        self.Subscription.create({
            'member_id': self.member.id,
            'plan_id': self.plan_monthly.id,
            'date_start': date.today(),
        })
        fclass = self.Class.create({
            'name': 'Yoga class',
            'trainer_id': self.trainer.id,
            'start_datetime': datetime.now() + timedelta(hours=1),
        })
        self.Attendance.create({
            'member_id': self.member.id,
            'class_id': fclass.id,
        })
        with self.assertRaises(Exception):
            with self.cr.savepoint():
                self.Attendance.create({
                    'member_id': self.member.id,
                    'class_id': fclass.id,
                })

    # 7. wizard
    def test_mass_renew_wizard(self):
        """Mass-renew wizard creates a subscription for each member."""
        m2 = self.Member.create({'partner_id': self.partner_b.id})
        wizard = self.env['mass.renew.subscription.wizard'].with_context(
            active_model='fitness.member',
            active_ids=[self.member.id, m2.id],
        ).create({
            'plan_id': self.plan_monthly.id,
            'date_start': date.today(),
        })
        wizard.action_apply()
        subs = self.Subscription.search([
            ('member_id', 'in', [self.member.id, m2.id]),
            ('plan_id', '=', self.plan_monthly.id),
        ])
        self.assertGreaterEqual(len(subs), 2)
