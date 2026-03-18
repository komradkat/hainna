from django.views.generic import TemplateView
from django.contrib.auth import get_user_model
from core.views import HtmxTemplateMixin

User = get_user_model()

class UserManagementView(HtmxTemplateMixin, TemplateView):
    template_name = 'users/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = User.objects.all().order_by('-date_joined')
        
        user_list = []
        for u in users:
            user_list.append({
                'id': f"U-{u.id:04d}",
                'initials': u.initials,
                'name': u.get_full_name() or u.username,
                'email': u.email,
                'role': u.role,
                'department': u.department or 'Unassigned',
                'position': u.position or 'N/A',
                'last_login': u.last_login.strftime('%b %d, %Y, %H:%M') if u.last_login else 'Never',
                'status': u.status,
            })
            
        context['users'] = user_list
        context['stats'] = {
            'total': users.count(),
            'active': users.filter(status='Active').count(),
            'admins': users.filter(role='Administrator').count(),
            'suspended': users.filter(status='Suspended').count()
        }
        return context

class AddUserView(HtmxTemplateMixin, TemplateView):
    template_name = 'users/form.html'

    def post(self, request, *args, **kwargs):
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        role = request.POST.get('role', 'Dispatcher')
        status = request.POST.get('status', 'Pending Verify')
        
        phone_number = request.POST.get('phone_number', '')
        department = request.POST.get('department', '')
        position = request.POST.get('position', '')
        date_of_hire = request.POST.get('date_of_hire', None) or None
        address = request.POST.get('address', '')
        emergency_contact_name = request.POST.get('emergency_contact_name', '')
        emergency_contact_number = request.POST.get('emergency_contact_number', '')

        if email:
            username = email.split('@')[0]
            if not User.objects.filter(username=username).exists():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password='defaultpassword123',
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    status=status,
                    phone_number=phone_number,
                    department=department,
                    position=position,
                    date_of_hire=date_of_hire,
                    address=address,
                    emergency_contact_name=emergency_contact_name,
                    emergency_contact_number=emergency_contact_number
                )
                
        # To reflect the update in the UI, we'll process the GET request of UserManagementView
        # HTMX handles the redirect and pushing URL correctly if set up properly,
        # but the simplest way to render the updated user list in HTMX swap is to just
        # instantiate UserManagementView and call get().
        list_view = UserManagementView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)
