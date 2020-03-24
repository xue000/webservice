from django.shortcuts import render,redirect,HttpResponse
from  django.contrib.auth import authenticate,login,logout
from  django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.db.models import Q
from .models import Professor, Module, List, Rate
import json

def login(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd= request.POST.get('pwd')
        user = authenticate(username=user,password=pwd)
        if user:
            auth.login(request,user)
            return  HttpResponse('Login successfully.')
        else:
            return HttpResponse('Fail to login.')
    return HttpResponse('None')

def logout(request):
    auth.logout(request)
    return HttpResponse('Logout.')

def reg(request):
    if request.method == 'POST':
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        email = request.POST.get('email')
        user = User.objects.create_user(username=user,password=pwd,email=email)
        user.save()
    return HttpResponse('Register.')

@login_required
def list(request):
    module_list = List.objects.all().values('module__mcode', 'module__mname', 'year', 'semester', 'professor__pid',
                                              'professor__pname')
    the_list = []
    for module in module_list:
        item = {'module_code': module['module__mcode'], 'module_name': module['module__mname'],
                'academic_years': module['year'], 'semester': module['semester'],
                'pid': module['professor__pid'], 'pname': module['professor__pname']}
        the_list.append(item)
    payload = {'module_list': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_pharse = 'OK'
    return http_response

@login_required
def view(request):
    rate = Rate.objects.all()
    the_list = []
    rate_list = []
    for i in rate:
        flag = 0
        a = len(the_list)
        for m in range(a):
            if (i.rp.pid == the_list[m][0]):
                flag = 1
                the_list[m][2] = (i.rate + the_list[m][2]) / 2
        if (flag == 0):
            the_list.append([i.rp.pid, i.rp.pname, i.rate])
    for i in the_list:
        item = {'pid': i[0], 'pname': i[1], 'rate': i[2]}
        rate_list.append(item)
    payload = {'rate_list': rate_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application/json'
    http_response.status_code = 200
    http_response.reason_pharse = 'OK'
    return http_response

@login_required
def average(request):
    if request.method == "POST":
        pro = request.POST.get('pro')
        module = request.POST.get('module')
        rate = Rate.objects.filter(Q(rp__pid=pro) & Q(rm__mcode=module))
        x = 0
        for i in rate:
            x = x + i.rate
            pname = i.rp.pname
            mname = i.rm.mname
        if (len(rate) == 0):
            x = 0
        else:
            x = x / len(rate)
        m = 'The rating of ' + pname + ' (' + pro + ') in module ' + mname + ' (' + module + ') is ' + str(x)
        return HttpResponse(m)

@login_required
def rate(request):
    if request.method == "POST":
        professor_id = request.POST.get('professor_id')
        module_code = request.POST.get('module_code')
        year = request.POST.get('year')
        semester = request.POST.get('semester')
        rating = request.POST.get('rating')
        rateprofessor = Professor.objects.get(pid=professor_id)
        ratemodule = Module.objects.get(mcode=module_code)
        rate = Rate.objects.create(rp = rateprofessor, rm = ratemodule, rate = int(rating))
        rate.save()
        if (rate):
            return HttpResponse("Success")
        else:
            return HttpResponse("Fail")

def wrong(request):
    return HttpResponse('Wrong')