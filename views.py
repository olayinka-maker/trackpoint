from django.shortcuts import render

from django.db.models import Count
from django.http import JsonResponse
from .models import Staff, Asset, AssetType, Department
from django.shortcuts import render, redirect
from .forms import UserForm, StaffForm, AssetForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def dashboard_overview(request):

    total_staff = Staff.objects.count()
    total_assets = Asset.objects.count()

    asset_types_data = AssetType.objects.annotate(count=Count('asset')).values(
        'name', 'count', 'color')

    # Assets by department for bar chart
    departments_data = Department.objects.annotate(
        asset_count=Count('asset')).values('name', 'asset_count')

    context = {
        "total_staff": total_staff or 0,
        "total_assets": total_assets or 0,
        "asset_types_data": asset_types_data,
        "departments_data": departments_data,
    }

    return render(request, 'dashboard.html', context)


def department_view(request):
    departments = Department.objects.all()
    context = {'departments': departments}
    return render(request, context)


def reports_view(request):
    reports = Asset.objects.all().order_by('-purchase_date')
    context = {'reports': reports}
    return render(request, 'reports.html', context)

    return render(request, 'reports.html', context)


def homepage(request):
    return render(request, 'home.html')


def login(request):
    return render(request, 'login_page.html')


def assets_view(request):
    assets = Asset.objects.select_related('asset_type', 'department',
                                          'assigned_to').all()
    departments = Department.objects.all()
    asset_type = AssetType.objects.all()

    all_assets = Asset.objects.all()
    context = {
        'all_assets': all_assets,
        'assets': assets,
        'departments': departments,
        'asset_type': asset_type
    }
    return render(request, 'assets.html', context)


def staff_view(request):
    staff = Staff.objects.select_related('user', 'department').all()
    staff_count = Staff.objects.count()
    all_staff = Staff.objects.all()

    context = {
        'staff_count': staff_count,
        'all_staff': all_staff,
        'staff': staff
    }
    return render(request, 'staff.html', context)


def chart_data_asset_types(request):
    data = AssetType.objects.annotate(count=Count('asset')).values(
        'name', 'count', 'color')
    return JsonResponse(list(data), safe=False)


def chart_data_departments(request):
    data = Department.objects.annotate(asset_count=Count('asset')).values(
        'name', 'asset_count')
    return JsonResponse(list(data), safe=False)


def create_staff(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        staff_form = StaffForm(request.POST)

        if user_form.is_valid() and staff_form.is_valid():
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            staff = staff_form.save(commit=False)
            staff.user = user
            staff.save()

            return redirect('staff')
    else:
        user_form = UserForm()
        staff_form = StaffForm()

    return render(request, 'register.html', {
        'user_form': user_form,
        'staff_form': staff_form
    })

    # def add_asset(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')
        location = request.POST.get('location')
        asset_type_id = request.POST.get('asset_type_id')
        department_id = request.POST.get('department_id')

        asset_type = AssetType.objects.get(
            id=asset_type_id) if asset_type_id else None
        department = Department.objects.get(
            id=department_id) if department_id else None

        Asset.objects.create(name=name,
                             asset_type=asset_type,
                             department=department,
                             status=status,
                             location=location)
        return redirect('assets')
    else:
        asset_types = AssetType.objects.all()
        departments = Department.objects.all()
        return render(request, 'add_asset.html', {
            'asset_types': asset_types,
            'departments': departments,
        })

    if request.method == 'POST':
        name = request.POST.get('name')
        status = request.POST.get('status')
        location = request.POST.get('location')
        asset_type_id = request.POST.get('asset_type_id')
        department_id = request.POST.get('department_id')
        assigned_to_id = request.POST.get('assigned_to_id')
        serial_number = request.POST.get('serial_number')
        purchase_date = request.POST.get('purchase_date')
        purchase_price = request.POST.get('purchase_price')

        asset_type = AssetType.objects.get(
            id=asset_type_id) if asset_type_id else None
        department = Department.objects.get(
            id=department_id) if department_id else None
        assigned_to = Staff.objects.get(
            id=assigned_to_id) if assigned_to_id else None

        Asset.objects.create(name=name,
                             asset_type=asset_type,
                             department=department,
                             assigned_to=assigned_to,
                             serial_number=serial_number,
                             purchase_date=purchase_date,
                             purchase_price=purchase_price,
                             status=status,
                             location=location)
        return redirect('assets')
    else:
        asset_types = AssetType.objects.all()
        departments = Department.objects.all()
        staff_members = Staff.objects.all()
        return render(
            request, 'add_asset.html', {
                'asset_types': asset_types,
                'departments': departments,
                'staff_members': staff_members
            })


# def add_asset(request):


def add_stock(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("assets")
    else:
        form = AssetForm()
    return render(request, "add_stock.html", {"form": form})
