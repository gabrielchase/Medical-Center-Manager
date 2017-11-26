from django.shortcuts import (render, redirect)
from django.views.generic import(TemplateView, View)
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.urls import reverse

from users.models import AdministratorDetails
from appointments.models import (
    Timeslot, Appointment
)
from dashboard.models import Service

User = get_user_model()


class AppointmentTemplate(TemplateView):
    template_name = 'appointments/create_appointment.html'

    def get_context_data(self, *args, **kwargs):
        context = super(AppointmentTemplate, self).get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context

    # def get(self, request, *args, **kwargs):
    #     print(kwargs.get('slug'))
    #     context = {}
        
    #     return render(request, self.template_name, context)

class AppointmentCreateDelete(View):

    def get(self, request, *args, **kwargs):
        aptmt_id = request.GET.get('aptmtid')
        slug = kwargs.get('slug')
        aptmt = Appointment.objects.get(appointment_id=aptmt_id)
        admin_user = User.objects.get(slug=slug)

        if aptmt.user == self.request.user and aptmt.admin.user == admin_user:
            aptmt.delete()
            messages.success(request, 'Successfully deleted your appointment')
        else:
            messages.error(request, 'Error in deleting your appointment')
            
        return redirect(reverse('users:detail', kwargs={'slug': slug}))

    def post(self, request, *args, **kwargs):
        if self.request.user.is_admin: 
            messages.error(request, 'You are an institution, you cannot make an appointment')
        else:
            # HANDLE ERROR FOR NOT UNIQUE TIMESLOT ON SAME DATE
            date = request.POST.get('date')
            timeslot_id = request.POST.get('timeslot')
            service_name = request.POST.get('service')  
            additional_info = request.POST.get('additional_info')
            slug = kwargs.get('slug')
            
            timeslot = Timeslot.objects.get(timeslot_id=timeslot_id)
            service = Service.objects.get(name=service_name)
            admin_user = User.objects.get(slug=slug)
            admin_instance = AdministratorDetails.objects.get(user=admin_user)

            Appointment.objects.create(
                date=date,
                status='Pending',
                admin=admin_instance,
                service=service, 
                timeslot=timeslot,
                user=self.request.user,
                additional_info=additional_info
            )
            messages.success(request, 'You have successfully made an appointment on {} from {} for {} at {}'
                                        .format(date, timeslot, service, admin_user.username))

        return redirect(reverse('users:detail', kwargs={'slug': slug}))
 

class AppointmentStatus(View):

    def get(self, request, *args, **kwargs):
        appointment_id = kwargs.get('appointment_id')
        status = request.GET.get('s')

        appointment = Appointment.objects.get(appointment_id=appointment_id)

        if appointment.admin.user == request.user:
            appointment.status = status
            appointment.save()

            messages.success(request, "Successfully set appointment with {} on {} at {} to '{}'"
                                        .format(appointment.user.username, appointment.date, appointment.timeslot, status.upper()))            
        else:
            print('Appointment admin and request.user are not the same')
            messages.error(request, "There was a problem with changing the appointment's status")
        
        return redirect(reverse('dashboard:home'))
