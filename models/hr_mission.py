# -*- utf-8 -*-
from openerp import models, fields, api, exceptions
from datetime import datetime


class HrMission(models.Model):
    _name = 'hr.mission'
    _description = 'Mission object'

    employee_id = fields.Many2one('hr.employee', string='Employee', help="Employee sent on mission", ondelete='cascade',
                                  required=True)
    mission_id = fields.Char(string='Reference', help="Mission reference. Define by company own organisation", size=20,
                             required=True)
    name = fields.Char(string='Mission Object', help="Mission aim task to do", size=80, required=True)
    mission_objective = fields.Text(string='Objective', help="Mission objective")
    mission_start_date = fields.Datetime(string="Start date",
                                         help="Mission start date", required=True)
    mission_end_date = fields.Datetime(string="End date", help="Mission end date", required=True)
    mission_partner = fields.Many2one('res.partner', string='Mission partner', required=True)
    mission_location = fields.Char(string='Partner mission location',
                                   help="Location where the mission will be take place")
    mission_partner_manager = fields.Many2one('res.partner', string='Partner mission manager',
                                              help="Responsible of this mission in partner company", required=True)
    mission_duration = fields.Char(compute='_get_duration', default=0, string="Duration", readonly=True)
    mission_evaluation = fields.Text(string='Evaluation')
    mission_notes = fields.Text(string='Notes')
    mission_car = fields.Selection([('pc', 'Personal car'), ('cc', 'Common car'),
                                    ('plane', 'Plane'), ('boat', 'Boat'),
                                    ('other', 'Other')], string="Locomotion")
    mission_type = fields.Many2one('hr.mission.type', string='Mission Type', required=False)
    mission_budget = fields.Float(string="Allocated Budget", help="Allocated budget for this mission", required=True)
    # Mission state for workflow implementation
    # mission_state = fields.Selection([
    #     ('draft', "Draft"),
    #     ('to_approved', "To Approve"),
    #     ('approved', "Approved"),
    #     ('rejected', "Rejected"),
    # ], default='draft')

    def get_own_missions(self, cr, uid, context=None):
        self.env.cr.execute('SELECT date FROM hr_mission_ where id=119')
        return self.env.cr.fetchone()

    @api.constrains('mission_end_date')
    @api.onchange('mission_start_date', 'mission_end_date')
    def _get_duration(self):
        for rec in self:
            if rec.mission_start_date and rec.mission_end_date:
                # get the date today as 2018-07-19
                td = datetime.now().strftime('%Y-%m-%d')
                today = datetime.strptime(td, "%Y-%m-%d")
                start = datetime.strptime(rec.mission_start_date, "%Y-%m-%d %H:%M:%S")

                if today.date() > start.date():
                    raise exceptions.ValidationError("Your mission start date must be higher or equal to"
                                                     " today date")

                if rec.mission_end_date > rec.mission_start_date:
                    time1 = datetime.strptime(rec.mission_start_date, "%Y-%m-%d %H:%M:%S")
                    time2 = datetime.strptime(rec.mission_end_date, "%Y-%m-%d %H:%M:%S")
                    delta = str(time2 - time1)
                    rec.mission_duration = delta
                else:
                    raise exceptions.ValidationError("Your mission end date must be higher than"
                                                     " mission start date ! %s" % rec.mission_end_date)

    # @api.multi
    # def action_draft(self):
    #     self.mission_state = 'draft'
    #
    # @api.multi
    # def action_to_approve(self):
    #     self.mission_state = 'to_approve'
    #
    # @api.multi
    # def action_approve(self):
    #     self.mission_state = 'approved'
    #
    # @api.multi
    # def action_reject(self):
    #     self.mission_state = 'rejected'
    @api.model
    def create(self, values):
        record = super(HrMission, self).create(values)
        return record


class HrEmployee(models.Model):
    _name = "hr.employee"
    _description = "Employee Category"
    _inherit = "hr.employee"

    in_mission = fields.Boolean(string="In Mission")
    missions_ids = fields.One2many('hr.mission', 'employee_id', string='Missions')


class HrExpense(models.Model):
    _name = 'hr.expense.expense'
    _description = "Expense"
    _inherit = 'hr.expense.expense'

    mission_id = fields.Many2one('hr.mission', 'Missions ID', help='Related mission if exist')


class HrMissionType(models.Model):
    _name = "hr.mission.type"
    _description = "Mission Type"

    name = fields.Char('Name', Required=True)
    description = fields.Char('Description', help='Describe this mission type aim !')
