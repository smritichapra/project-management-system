from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
urlpatterns = [
    path('',views.main,name='main'),
    path('ctasks/', views.ctasks, name='ctasks'),
    path('cnotification/', views.cnotification, name='cnotification'),
    path('creport/', views.creport, name='creport'),
    path('cdashboard/',views.cdashboard,name='cdashboard'),
    path('clogin/',views.clogin,name='clogin'),
    path('cproposals/',views.cproposals,name='cproposals'),
    path('cmarks/',views.cmarks,name='cmarks'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('login/',views.login,name='login'),
    path('Mlogin/',views.Mlogin,name='Mlogin'),
    path('project/<int:team_id>/', views.Mproject, name='Mproject'),
    path('notification/',views.notification,name='notification'),
    path('report/',views.report,name='report'),
    path('signup/',views.signup,name='signup'),
    path('tasks/',views.tasks,name='tasks'),
    path('tdashboard/',views.tdashboard,name='tdashboard'),
    path('tgroups/',views.tgroups,name='tgroups'),
    path('tlogin/',views.tlogin,name='tlogin'),
    path('tnotification/',views.tnotification,name='tnotification'),
    path('tproject/',views.tproject,name='tproject'),
    path('treport/',views.treport,name='treport'),
    path('tsignup/',views.tsignup,name='tsignup'),
    path('ttasks/',views.ttasks,name='ttasks'),
    path('tsignup_success/',views.tsignup_success,name='tsignup_success'),
    path('tteamdetails/',views.tteamdetails,name='tteamdetails'),
    path('add_task/',views.add_task,name='add_task'),
    path('Mmarks/',views.Mmarks,name='Mmarks'),
    path('upload_task/<int:task_id>/', views.upload_task_file, name='upload_task'),
    path('upload_marks/',views.upload_marks,name='upload_marks'),
    
    path("update_marks/<int:team_id>/", views.update_marks, name="update_marks"),
    path('update_project/<int:project_id>/<str:status>/', views.update_project_status, name='update_project'),
]




