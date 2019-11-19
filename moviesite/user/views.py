from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django import forms
from .models import User

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['age', 'sex', 'interests']
        
@login_required
def profile_view(request):
    return render(request, 'account/profile.html')

@login_required
def change_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        form.save()
        messages.add_message(request,messages.SUCCESS,'个人信息更新成功！')
        return redirect('user:profile')
    else:
    # 不是POST请求就返回空表单
        form = ProfileForm(instance=request.user)
        return render(request,'account/profile_change.html',context={'form':form})
    return render(request, 'account/profile_change.html')


