from django.urls import path
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='home'),  # Landing page
    path('login/',
         auth_views.LoginView.as_view(template_name='login_page.html'),
         name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_overview, name='dashboard'),
    path('assets/', views.assets_view, name='assets'),
    path('staff/', views.staff_view, name='staff'),
    path('reports/', views.reports_view, name='reports'),
    path('api/chart/asset-types/',
         views.chart_data_asset_types,
         name='chart_asset_types'),
    path('api/chart/departments/',
         views.chart_data_departments,
         name='chart_departments'),
    path('create-staff/', views.create_staff, name='register'),
    path('add-asset/', views.add_stock, name='add_asset'),
    path('report/', views.reports_view, name='report'),
]
