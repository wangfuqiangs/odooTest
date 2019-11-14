# -*- coding: utf-8 -*-

from odoo import models, fields, api


# 关联字段
class TodoCategory(models.Model):
    _name = 'todo.category'
    _description = '分类'

    name = fields.Char('名称')
    task_ids = fields.One2many('todo.task', 'category_id', string='待办事项')
    count = fields.Integer('任务数量', compute='_compute_task_count')

    @api.depends('task_ids')
    @api.multi
    def _compute_task_count(self):
        for record in self:
            record.count = len(record.task_ids)


# 开始字段
class TodoTesk(models.Model):
    _name = 'todo.task'
    _description = '待办事项'

    name = fields.Char('描述', required=True)
    is_done = fields.Boolean('已完成')

    # 选择字段
    xuanxiang = fields.Selection([
        ('todo', '代办'),
        ('yiban', '一般'),
        ('zhaoji', '着急')
    ], default='todo', string='紧急程度')

    # 日期字段
    riqi = fields.Datetime(u'截止时间')

    # 计算字段与视图装饰器
    is_expired = fields.Boolean(u'已经过期了', compute='_computer_is_expired')

    @api.depends('riqi')
    @api.multi
    def _computer_is_expired(self):
        for record in self:
            if record.riqi:
                record.is_expired = record.riqi < fields.Datetime.now()
            else:
                record.is_expired = False

    category_id = fields.Many2one('todo.category', string='分类')
