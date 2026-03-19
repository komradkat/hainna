from django.views.generic import TemplateView, View
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from core.views import HtmxTemplateMixin, DashboardView
from .forms import UserForm

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
                'pk': u.pk,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm()
        context['is_edit'] = False
        return context

    def post(self, request, *args, **kwargs):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            # Return fresh list
            list_view = UserManagementView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        # If invalid, re-render form with errors
        return render(request, self.template_name, {
            'form': form,
            'is_edit': False,
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class EditUserView(HtmxTemplateMixin, TemplateView):
    template_name = 'users/form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        context['form'] = UserForm(instance=user)
        context['is_edit'] = True
        context['user_id'] = f"U-{user.id:04d}"
        return context

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Return fresh list
            list_view = UserManagementView()
            list_view.request = request
            list_view.kwargs = kwargs
            list_view.args = args
            return list_view.get(request, *args, **kwargs)
        
        return render(request, self.template_name, {
            'form': form,
            'is_edit': True,
            'user_id': f"U-{user.id:04d}",
            'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
        })

class DeleteUserView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(User, pk=self.kwargs.get('pk'))
        user.delete()
        
        # Return updated list or just empty response for HTMX removal
        # In this case, standard behavior is to refresh the list or remove row.
        # Let's return the refreshed UserManagementView
        list_view = UserManagementView()
        list_view.request = request
        list_view.kwargs = kwargs
        list_view.args = args
        return list_view.get(request, *args, **kwargs)

class ChangePasswordView(HtmxTemplateMixin, TemplateView):
    template_name = 'users/change_password.html'

    def post(self, request, *args, **kwargs):
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not request.user.check_password(current_password):
            return render(request, self.template_name, {
                'error': 'Current password incorrect',
                'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
            })

        if new_password != confirm_password:
            return render(request, self.template_name, {
                'error': 'Passwords do not match',
                'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
            })
        
        if len(new_password) < 8:
            return render(request, self.template_name, {
                'error': 'Password must be at least 8 characters',
                'base_template': 'partial_base.html' if request.headers.get('HX-Request') else 'base.html'
            })

        request.user.set_password(new_password)
        request.user.requires_password_change = False
        request.user.save()
        
        # Log the user back in since set_password logs them out
        update_session_auth_hash(request, request.user)

        dashboard = DashboardView()
        dashboard.request = request
        dashboard.kwargs = kwargs
        dashboard.args = args
        return dashboard.get(request, *args, **kwargs)
