"""
URL configuration for BROKER project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from API import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='get_token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='refresh'),
    path('api/job/query-home-jobs/', views.QueryHomeJobs.as_view(), name='Query home jobs'),
    path('api/job/query-job-card/', views.QueryJobCard.as_view(), name='Query job card'),
    path('api/job/quick-set/completed/', views.QuickEditJobstatus.as_view(), name='Quick set job completed status'),
    path('api/job/update/', views.QuickEditJobCardFields.as_view(), name='Quick update of the job card'),
    path('api/job/new/', views.QueryNewJob.as_view(), name='Create new job'),
    path('api/job/delete/', views.QueryDeleteJob.as_view(), name='Delete job'),
    path('api/job/query-time-table/', views.QueryTimeTable.as_view(), name='Query time table'),
    path('api/job/query-time-table/update/', views.QuickEditTimeEntry.as_view(), name='Quick edit time entry'),
    path('api/job/query-time-table/add/', views.AddTimeEntry.as_view(), name='Add time entry'),
    path('api/job/query-time-table/delete/', views.DeleteTimeEntry.as_view(), name='Delete time entry'),
    path('api/job/query-part-table/', views.QueryPartsTable.as_view(), name='Query part table'),
    path('api/job/query-part-table/update/', views.QuickEditPartEntry.as_view(), name='Quick edit part entry'),
    path('api/job/query-part-table/add/', views.AddPartEntry.as_view(), name='Add part entry'),
    path('api/job/query-part-table/delete/', views.DeletePartEntry.as_view(), name='Delete part entry'),
    path('api/customers/query-customers/', views.QueryCustomersTable.as_view(), name='Query customer table'),
    path('api/customers/query-customer-card/', views.QueryCustomerCard.as_view(), name='Query customer card'),
    path('api/customers/query-customers/update/', views.QuickEditCustomerEntry.as_view(), name='Quick edit customer entry'),
    path('api/customers/query-customers/add/', views.AddCustomerEntry.as_view(), name='Add customer entry'),
    path('api/customers/query-customers/delete/', views.DeleteCustomerEntry.as_view(), name='Delete customer entry'),
    path('api/site-settings/query-settings/', views.QuerySiteSettings.as_view(), name='Query site settings'),
]
