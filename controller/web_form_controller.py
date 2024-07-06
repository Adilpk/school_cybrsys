# -*- coding: utf-8 -*-
from odoo.http import Controller, request, route


class WebFormController(Controller):

    @route('/studentform', auth='public', website=True)
    def student_form(self, **kwargs):
        """ when click registration menu it will move into this route and
             render the students details template"""
        students = request.env['student.manage'].sudo().search([])
        return request.render('school_management.web_students_template',
                              {'students': students})

    @route('/createstudent', auth='public', website=True)
    def create_student(self, **post):
        """ when click register student it will move into form template
         for register student """
        depart = request.env['manage.department'].search([])
        classes = request.env['manage.class'].search([])
        values = {
            'department': depart,
            'class': classes
        }
        return request.render('school_management.web_form_template', values)

    @route('/studentform/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def web_form_submit(self, **post):
        """ when submit the students details it will store the database and its
         redirect to students details template  """
        request.env['student.manage'].sudo().create({
                    'first_name': post.get('first_name'),
                    'last_name': post.get('last_name'),
                    'email': post.get('email'),
                    'communication_address': post.get('communication_address'),
                    'phone': post.get('phone'),
                    'date_of_birth': post.get('date_of_birth'),
                    'father': post.get('father'),
                    'mother': post.get('mother'),
                    'department_id': post.get('department_id'),
                    'class_id': post.get('class_id'),
                    'filename': post.get('filename'),
                    'aadhar_number': post.get('aadhar_number'),
                })
        return request.redirect('/studentform')

    @route('/eventform', auth='public', website=True)
    def event_form(self, **kwargs):
        """ it show all events details in the template"""
        events = request.env['manage.events'].sudo().search([])
        return request.render('school_management.web_all_events_template',
                              {'events': events})

    @route('/createevents', auth='public', website=True)
    def create_events(self, **post):
        """ and we can create new events from this form"""
        club = request.env['manage.clubs'].search([])
        company = request.env.user.company_id
        values = {
            'clubs': club,
            'company': company
        }
        return request.render('school_management.web_event_template', values)

    @route('/eventform/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def event_form_submit(self, **post):
        """ when submit the events form it will store the
         events details into database  and redirect into
         event details template"""
        request.env['manage.events'].sudo().create({
            'club_id': post.get('club_name'),
            'event_card': post.get('event_card'),
            'venue_id': post.get('venue'),
            'name': post.get('event'),
            'coordinator': post.get('coordinator'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date')
        })
        return request.redirect('/eventform')

    @route('/leaveform', auth='public', website=True)
    def web_form(self, **kwargs):
        """ it will show all the leaves and render the template"""
        leaves = request.env['manage.leaves'].sudo().search([])
        return request.render('school_management.web_all_leaves_template',
                              {'leaves': leaves})

    @route('/createleave', auth='public', website=True)
    def create_leave(self, **post):
        """ it will render the leave form template"""
        current_user = request.env.user
        print(current_user)
        return request.render('school_management.web_leave_template',
                              {'current_user': current_user})

    @route('/leaveform/submit', type='http', auth='public', website=True,
           methods=['POST'])
    def leave_form_submit(self, **post):
        """ it will store the values in to database and e render the
         leave details template"""
        request.env['manage.leaves'].sudo().create({
            'subject': post.get('subject'),
            'student_id': post.get('student'),
            'start_date': post.get('start_date'),
            'end_date': post.get('end_date'),
        })
        return request.redirect('/leaveform')








