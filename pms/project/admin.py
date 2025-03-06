from django.contrib import admin
from .models import Signup
from .models import Team, TeamMember
from .models import GroupDetails, Marks, ProjectDetails
from .models import  Coordinator, Mentor, Task
# Customize the display in the admin panel
class SignupAdmin(admin.ModelAdmin):
    list_display = ('id', 'uname', 'uemail', 'ucontact', 'upassword')  # Columns to display in the admin list view
    search_fields = ('uname', 'uemail', 'ucontact')  # Fields to enable search functionality
    list_filter = ('uemail',)  # Fields to enable filtering
    ordering = ('id',)  # Default ordering of records
    list_per_page = 20  # Number of records to show per page

# Register the model and the custom admin class
admin.site.register(Signup, SignupAdmin)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_id', 'team_name','password')  # Display these fields in the admin list view
    search_fields = ('team_id', 'team_name')  # Add search functionality for these fields
admin.site.register(Team,TeamAdmin)

class CoordinatorAdmin(admin.ModelAdmin):
    list_display = ('coord_name', 'c_email', 'phone_no','password')
    search_fields = ('coord_name', 'c_email')
admin.site.register(Coordinator,CoordinatorAdmin)


class MentorAdmin(admin.ModelAdmin):
    list_display = ('m_email', 'mentor_name', 'phone_no')
    search_fields = ('mentor_name', 'm_email')
admin.site.register(Mentor,MentorAdmin)


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('stu_id', 'member_name', 'student_class', 'branch', 'semester', 'stu_rollno', 'phone_no', 'email','team_id')  # Display these fields
    search_fields = ('stu_id', 'member_name', 'email', 'team_name', 'team_id')  # Add search functionality
    list_filter = ('branch', 'semester')  # Add filters for these fields
    raw_id_fields = ('team_id',) 
admin.site.register(TeamMember,TeamMemberAdmin)


class GroupDetailsAdmin(admin.ModelAdmin):
    list_display = ('group_id', 'mentor_name', 'project_name', 'team_id')
    search_fields = ('group_id', 'mentor_name', 'project_name')

admin.site.register(GroupDetails,GroupDetailsAdmin)

class MarksAdmin(admin.ModelAdmin):
    list_display = ('stu_rollno', 'marks', 'member_name', 'stu_id')
    search_fields = ('stu_rollno', 'member_name', 'stu_id')
admin.site.register(Marks,MarksAdmin)
# Register ProjectDetails Model

class ProjectDetailsAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_name', 'team_id', 'approval')
    search_fields = ('project_id', 'project_name', 'team_id')
admin.site.register(ProjectDetails,ProjectDetailsAdmin)

class TaskAdmin(admin.ModelAdmin):
    list_display = ('task_id', 'doc_title', 'status', 'start_date', 'end_date', 'm_email')
    search_fields = ('doc_title',)
    list_filter = ('status',)
    
admin.site.register(Task,TaskAdmin)