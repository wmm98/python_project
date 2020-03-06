from django.shortcuts import render, redirect, reverse
from ..xfzauth.models import User
from django.views.generic import View
from django.contrib.auth.models import Group
from ..xfzauth.decorators import xfz_superuser_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.views.decorators.http import require_POST, require_GET
from ..utils import restful


@xfz_superuser_required
def staffs_view(request):
    staffs = User.objects.filter(is_staff=True)
    context = {
        'staffs': staffs
    }
    return render(request, 'cms/staffs.html', context=context)


@method_decorator(xfz_superuser_required, name='dispatch')
class AddStaffView(View):
    def get(self, request):
        groups = Group.objects.all()
        context = {
            'groups': groups
        }
        return render(request, 'cms/add_staff.html', context=context)

    def post(self, request):
        telephone = request.POST.get('telephone')
        user = User.objects.filter(telephone=telephone).first()
        if user:
            user.is_staff = True
            group_ids = request.POST.getlist("groups")
            groups = Group.objects.filter(pk__in=group_ids)
            user.groups.set(groups)
            user.save()
            return redirect(reverse('cms:staffs'))
        else:
            messages.info(request, '手机号码不存在！')
            return redirect(reverse('cms:add_staff'))


@require_POST
@permission_required(perm="xfzauth.change_user", login_url='/')
def delete_staff(request):
    staff_id = request.POST.get('staff_id')
    User.objects.filter(pk=staff_id).update(is_staff=False)
    return restful.ok()
