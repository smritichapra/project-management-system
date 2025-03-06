from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.shortcuts import render, redirect
from .models import Mteam, ProjectDetails, Team, TeamMember, Mentor, GroupDetails,Ttask,Marks
from django.db import transaction
# Create your views here.
from django.core.exceptions import ValidationError
from .models import Signup
from django.contrib import messages
from .models import Team
from django.db.models import OuterRef, Subquery
from .models import TeamMember,Mentor,Coordinator
from django.db import IntegrityError
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from .models import ProjectDetails
from django.http import JsonResponse
from .models import Task
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import mimetypes


def open_file(request, file_path):
    file_abs_path = os.path.join(settings.MEDIA_ROOT, file_path)
    
    if os.path.exists(file_abs_path):
        mime_type, _ = mimetypes.guess_type(file_abs_path)
        with open(file_abs_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type=mime_type)
            response['Content-Disposition'] = 'inline'  # 👈 Force Open Instead of Download
            return response
    else:
        return HttpResponse("File not found", status=404)
def main(request):
    return render(request, 'mentor/main.html')



def cdashboard(request):
    # Check if coordinator is logged in
    if 'coordinator_email' not in request.session:
        messages.error(request, "You must log in to access this page.")
        return redirect('clogin')

    if request.method == 'POST':
        c_email = request.session['coordinator_email']
        team_id = request.POST.get('team_id')
        mentor_email = request.POST.get('mentor_id')
        group_id = request.POST.get('group_id')

        try:
            team = Team.objects.get(team_id=team_id)
            mentor = Mentor.objects.get(m_email=mentor_email)
            project_details = ProjectDetails.objects.filter(team_id=team_id).first()
            project_name = project_details.project_name if project_details else "No Project"

            GroupDetails.objects.create(
                group_id=group_id,
                mentor_name=mentor.mentor_name,
                project_name=project_name,
                m_email=mentor,
                c_email=Coordinator.objects.get(c_email=c_email),
                team_id=team,
            )

            mteam = Mteam.objects.get(team_id=team_id)
            mteam.m_email_id = mentor_email
            mteam.save()

            messages.success(request, "Group details saved and mentor email updated successfully!")
        except Exception as e:
            messages.error(request, f"Error saving group details: {str(e)}")

        return redirect('cdashboard')

    # Fetch all teams with related data
    teams = Team.objects.all()
    data = []

    for team in teams:
        team_id = team.team_id

        # Fetch team members
        team_members = TeamMember.objects.filter(team_id=team_id)
        members = [{
            'stu_id': member.stu_id,
            'member_name': member.member_name,
            'student_class': member.student_class,
            'branch': member.branch,
            'semester': member.semester,
            'stu_rollno': member.stu_rollno,
            'phone_no': member.phone_no,
            'email': member.email,
        } for member in team_members]

        # Fetch project details
        project_details = ProjectDetails.objects.filter(team_id=team_id).first()
        project_name = project_details.project_name if project_details else "No Project"

        # Fetch allocated mentor and group ID
        group_details = GroupDetails.objects.filter(team_id=team_id).first()
        allocated_mentor = group_details.mentor_name if group_details else None
        group_id = group_details.group_id if group_details else None

        # Append the fetched data to the list
        data.append({
            'team_id': team_id,
            'team_name': team.team_name,
            'members': members,
            'project_name': project_name,
            'allocated_mentor': allocated_mentor,
            'group_id': group_id,
        })

    # Fetch all mentors
    mentors = Mentor.objects.all()

    # Pass the data to the template
    context = {
        'data': data,
        'mentors': mentors,
    }

    return render(request, 'mentor/cdashboard.html', context)
def clogin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            coordinator = Coordinator.objects.get(c_email=email)  # Fetch Coordinator
            if password == coordinator.password:  # Direct password comparison
                request.session['coordinator_email'] = coordinator.c_email  # Store session data
                messages.success(request, "Login successful!")
                return redirect('cdashboard')  # Redirect to dashboard
            else:
                messages.error(request, "Invalid credentials")
        except Coordinator.DoesNotExist:
            messages.error(request, "Invalid credentials")
    return render(request, 'mentor/clogin.html')

def add_task(request):
    if request.method == 'POST':
        # ✅ Corrected the .get() method calls
        doc_title = request.POST.get('document-title')
        start_date = request.POST.get('start-date')
        end_date = request.POST.get('end-date')
        description = request.POST.get('description', '')  # Default to empty string
        m_email = request.session.get("mentor_email")  # Assuming email is stored in session
        file = request.FILES.get('file-upload')

        try:
            # ✅ Ensure the mentor exists
            mentor = Mentor.objects.get(m_email=m_email)  
            
            # ✅ Handle file upload
            file_url = None
            fs = FileSystemStorage()  # Save in "media/uploads"
            filename = fs.save(file.name, file)
            file_url = f"/{filename}" 
            # ✅ Create the Task
            Task.objects.create(
                doc_title=doc_title,
                status="Pending",
                file_upload=file_url,  # ✅ Corrected from `file_uplod`
                start_date=start_date,
                end_date=end_date,
                m_email=mentor,  # ✅ Ensure this is a Mentor object
                description=description,
            )

            messages.success(request, "Task added successfully!")
            return redirect('tasks')

        except Mentor.DoesNotExist:
            print("⚠ Mentor entry not found for user!")  # Debugging output
            messages.error(request, "Mentor not found. Please log in again.")
            return redirect('login')

    return redirect('tasks')

def upload_file(request, task_id):
    if request.method == 'POST' and request.FILES.get('file'):
        task = Task.objects.get(task_id=task_id)
        task.file_upload = request.FILES['file']  # Store in upload_file field
        task.save()
        return redirect('ttasks')  # Redirect to task page after upload
    return redirect('ttasks')
def cnotification(request):
    return render(request, 'mentor/cnotification.html')

def cproposals(request):
    # Subquery to fetch the team name based on team_id
    team_subquery = Team.objects.filter(team_id=OuterRef('team_id')).values('team_name')[:1]

    # Annotate each project with the corresponding team name
    projects = ProjectDetails.objects.annotate(team_name=Subquery(team_subquery)).all()

    return render(request, 'mentor/cproposals.html', {'projects': projects})
def update_project_status(request, project_id, status):
    project = get_object_or_404(ProjectDetails, project_id=project_id)
    project.approval = status
    project.save()
    return redirect('cproposals')  # Redirect to proposals page after updating
def creport(request):
    return render(request, 'mentor/creport.html')

def cmarks(request):
    teams = Team.objects.all()  
    team_data = []

    for team in teams:
        members = TeamMember.objects.filter(team_id=team.team_id)
        member_data = []
        
        for member in members:
            marks_entry = Marks.objects.filter(stu_id=member).first()
            member_data.append({
                "stu_rollno": member.stu_id,
                "name": member.member_name,
                "email": member.email,
                "mentor_marks": marks_entry.marks if marks_entry else "",
                "coordinator_marks": marks_entry.coordinator_marks if marks_entry else "",
                "percentage": marks_entry.percentage if marks_entry else "",
                "grade": marks_entry.grade if marks_entry else "",
            })

        team_data.append({
            "team_id": team.team_id,
            "team_name": team.team_name,
            "members": member_data
        })

    return render(request, "mentor/cmarks.html", {"teams": team_data})


def update_marks(request,team_id):
     if request.method == "POST":
        members = TeamMember.objects.filter(team_id=team_id)
        
        for member in members:
            key = f"coordinator_marks_{member.stu_id}"
            if key in request.POST:
                coordinator_marks = request.POST[key]

                marks_entry, created = Marks.objects.get_or_create(stu_id=member)

                # Update marks, calculate percentage & grade
                marks_entry.coordinator_marks = int(coordinator_marks) if coordinator_marks else None
                if marks_entry.marks is not None and marks_entry.coordinator_marks is not None:
                    total_marks = marks_entry.marks + marks_entry.coordinator_marks
                    marks_entry.percentage = total_marks / 2
                    marks_entry.grade = (
                        "A+" if total_marks >= 90 else
                        "A" if total_marks >= 80 else
                        "B" if total_marks >= 70 else
                        "C" if total_marks >= 60 else
                        "D" if total_marks >= 50 else "F"
                    )
                marks_entry.save()

        return redirect("cmarks")

     return redirect("cmarks")
def ctasks(request):
    return render(request, 'mentor/ctasks.html')
def dashboard(request):
    if 'mentor_email' not in request.session:
        messages.error(request, "You must log in to access this page.")
        return redirect('mentor_login')  # Redirect to mentor login page if not logged in

    # Get the logged-in mentor's email from the session
    mentor_email = request.session['mentor_email']

    try:
        # Fetch the mentor's details
        mentor = Mentor.objects.get(m_email=mentor_email)

        # Fetch teams allocated to the mentor using GroupDetails
        allocated_teams = GroupDetails.objects.filter(m_email=mentor)

        # Initialize a list to store team details
        team_details = []

        # Loop through each allocated team
        for group in allocated_teams:
            team = group.team_id  # Get the team object
            team_members = TeamMember.objects.filter(team_id=team.team_id)  # Fetch team members

            # Append team details to the list
            team_details.append({
                'team_name': team.team_name,
                'team_id': team.team_id,
                'members': [
                    {
                        'sno': idx + 1,
                        'name': member.member_name,
                        'class': member.student_class,
                        'branch': member.branch,
                        'stu_id': member.stu_id,
                        'email': member.email,
                        'phone_no': member.phone_no,
                        'semester': member.semester,
                        'roll_no': member.stu_rollno,
                    }
                    for idx, member in enumerate(team_members)
                ]
            })

        # Pass the data to the template
        context = {
            'mentor_name': mentor.mentor_name,
            'team_details': team_details,
        }

        return render(request, 'mentor/dashboard.html', context)

    except Exception as e:
        messages.error(request, f"Error fetching team details: {str(e)}")
        return redirect('dashboard')
    
    
def login(request):
    return render(request, 'mentor/login.html')

def Mlogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            mentor = Mentor.objects.get(m_email=email)  # Fetch mentor from DB
            if password==mentor.password:  # Verify password
                request.session["mentor_email"] = mentor.m_email  # Store session data
                messages.success(request, "Login successful!")
                return redirect('dashboard') # Redirect to dashboard
            else:
                messages.error(request, "Invalid password.")  # Incorrect password

        except Mentor.DoesNotExist:
            messages.error(request, "No account found with this email.")
    return render(request, 'mentor/Mlogin.html')
def Mmarks(request):
    mentor_email = request.session.get('mentor_email')
    if not mentor_email:
        return redirect('Mlogin')  # Redirect if mentor is not logged in

    # Fetch mentor object
    try:
        mentor = Mentor.objects.get(m_email=mentor_email)
    except Mentor.DoesNotExist:
        messages.error(request, 'Mentor not found')
        return redirect('Mlogin')

    # Fetch teams assigned to the mentor
    mteams = Mteam.objects.filter(m_email=mentor)
    teams = Team.objects.filter(team_id__in=mteams.values_list('team_id', flat=True))

    # Fetch team members for those teams
    team_members = TeamMember.objects.filter(team_id__in=teams.values_list('team_id', flat=True))

    # Fetch existing marks for these team members
    marks_data = Marks.objects.filter(stu_id__in=team_members.values_list('stu_id', flat=True))

    # Create a dictionary to map student IDs to their marks
    marks_dict = {mark.stu_id_id: mark.marks for mark in marks_data}

    # Debugging output to verify data retrieval
    print(f"Mentor: {mentor}")
    print(f"Assigned Teams: {list(teams.values())}")
    print(f"Team Members: {list(team_members.values())}")
    print(f"Marks Data: {list(marks_data.values())}")

    # Pass data to the template
    context = {
        'teams': teams,
        'team_members': team_members,
        'marks_dict': marks_dict,  # Pass marks data to the template
    }
    return render(request, 'mentor/Mmarks.html', context)
def upload_marks(request):
    if request.method == 'POST':
        # Fetch mentor email from session
        mentor_email = request.session.get('mentor_email')
        if not mentor_email:
            messages.error(request, 'Not logged in')
            return redirect('Mlogin')

        # Fetch mentor object
        try:
            mentor = Mentor.objects.get(m_email=mentor_email)
        except Mentor.DoesNotExist:
            messages.error(request, 'Mentor not found')
            return redirect('Mlogin')

        # Fetch teams assigned to the mentor using the Mteam model
        mteams = Mteam.objects.filter(m_email=mentor)
        teams = Team.objects.filter(team_id__in=[mteam.team_id.team_id for mteam in mteams])
        
        # Fetch team members for those teams
        team_members = TeamMember.objects.filter(team_id__in=teams)

        # Iterate through team members and save marks
        for member in team_members:
            marks = request.POST.get(f'marks_{member.stu_id}')
            if marks:
                # Update or create marks entry for each student
                Marks.objects.update_or_create(
                    stu_id=member,
                    defaults={
                        'stu_rollno': member.stu_id,
                        'marks': marks,
                        'member_name': member.member_name,
                        'stu_id': member,
                 # Assuming coordinator is a field in Team
                        'm_email': mentor,
                    }
                )

        # Show success message and redirect
        messages.success(request, 'Marks uploaded successfully')
        return redirect('Mmarks')

    # If the request method is not POST, show an error
    messages.error(request, 'Invalid request method')
    return redirect('dashboard')
def Mproject(request,team_id):
    team = Team.objects.get(team_id=team_id)
    project = ProjectDetails.objects.get(team_id=team_id)  # Assuming each team has one project
    context = {
        'project_name': project.project_name,
        'project_description': project.description,
        'tech_stack': project.tech_stack,
    }
    return render(request, 'mentor/Mproject.html', context)

def notification(request):
    return render(request, 'mentor/notification.html')

def report(request):
    return render(request, 'mentor/report.html')

def signup(request):
    if request.method == "POST":
        mentor_name = request.POST.get("mentor-name")
        email = request.POST.get("email")
        password = request.POST.get("password")  # Should be stored securely
        phone = request.POST.get("phone")
        confirm_password = request.POST.get("confirm_password")
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "mentor/signup.html")
        try:
            # Save mentor details in database
            mentor = Mentor.objects.create(
                m_email=email,
                phone_no=phone,
                mentor_name=mentor_name,
                password=password
                
            )
            mentor.save()
            messages.success(request, "Signup successful! Please login.")
            return redirect("Mlogin")  # Redirect to login page

        except IntegrityError:
            messages.error(request, "Email already registered. Try logging in.")
    return render(request, 'mentor/signup.html')

def tasks(request):
    m_email = request.session.get("mentor_email") 
    if not m_email:
        messages.error(request, "Session expired! Please log in again.")
        return redirect('login')

    try:
        # Get the mentor instance
        mentor = Mentor.objects.get(m_email=m_email)

        # Retrieve tasks assigned to the logged-in mentor
        tasks = Task.objects.filter(m_email=mentor)

        # Retrieve submissions for each task
        submissions = {}
        for task in tasks:
            ttasks = Ttask.objects.filter(task_id_id=task.task_id)  # Filter by task_id_id
            submissions[task.task_id] = list(ttasks)

        # Debugging output
        print("Tasks:", tasks)
        print("Submissions:", submissions)

        return render(request, 'mentor/tasks.html', {
            'tasks': tasks,
            'submissions': submissions,
        })

    except Mentor.DoesNotExist:
        messages.error(request, "Mentor not found! Please log in again.")
        return redirect('login')
    
def tteamdetails(request):
    if request.method == "POST":
        stu_id = request.POST.get("stu_id")
        member_name = request.POST.get("member_name")
        student_class = request.POST.get("student_class")
        branch = request.POST.get("branch")
        semester = request.POST.get("semester")
        stu_rollno = request.POST.get("stu_rollno")
        phone_no = request.POST.get("phone_no")
        email = request.POST.get("email")

        # Get team_id from session
        team_id = request.session.get("team_id")
        if not team_id:
            messages.error(request, "You must be logged in as a team to add members.")
            return redirect("tlogin")  # Redirect to login if session is missing

        try:
            team = Team.objects.get(team_id=team_id)
            TeamMember.objects.create(
                stu_id=stu_id,
                member_name=member_name,
                student_class=student_class,
                branch=branch,
                semester=semester,
                stu_rollno=stu_rollno,
                phone_no=phone_no,
                email=email,
                team_id=team
            )
            messages.success(request, "Team member added successfully!")
            return redirect("tdashboard")  # Redirect to dashboard after successful submission
        except ValidationError as e:
            messages.error(request, "you can't have more than 5 members")
            return redirect("tdashboard")
            
            
        except Team.DoesNotExist:
            messages.error(request, "Invalid Team ID.")
            return redirect("tlogin")
    return render(request,'mentor/tteamdetails.html')
def tdashboard(request):
    team_id = request.session.get("team_id")  # Modify this based on where team_id is stored

    # Fetch members belonging to this team
    team_members = TeamMember.objects.filter(team_id=team_id)
    
    return render(request, 'mentor/tdashboard.html', {'team_members': team_members})
    

def tsignup_success(request):
    return render(request, 'mentor/tsignup_success.html')

def tgroups(request):
    return render(request, 'mentor/tgroups.html')

def tlogin(request):
    if request.method == "POST":
        team_id = request.POST.get("team_id")
        password = request.POST.get("password")

        try:
            team = Team.objects.get(team_id=team_id)  # Get team by ID
            if team.password == password:  # Directly compare password (NO HASHING)
                request.session["team_id"] = team_id  # Store session
                return redirect("tdashboard")  # Redirect to dashboard
            else:
                return render(request, "mentor/tlogin.html", {"error": "Invalid Password"})
        except Team.DoesNotExist:
            return render(request, "mentor/tlogin.html", {"error": "Team not found"})

    return render(request, 'mentor/tlogin.html')

def tnotification(request):
    return render(request, 'mentor/tnotification.html')

def tproject(request):
    if request.method == 'POST':
        project_name = request.POST.get('projectName')  # Match HTML field names
        description = request.POST.get('description')
        tech_stack = request.POST.get('techStack')
        team_id = request.session.get("team_id")
        if project_name and description and tech_stack:
            ProjectDetails.objects.create(
                project_name=project_name,
                description=description,
                tech_stack=tech_stack,
                team_id=team_id
            )# Return success response
            return redirect('tdashboard')
    return render(request, 'mentor/tproject.html')

def treport(request):
    return render(request, 'mentor/treport.html')

def tsignup(request):
    if request.method == "POST":
        team_name = request.POST.get("team_name")
        email = request.POST.get("email")  # Get email from frontend
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if any field is empty
        if not team_name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return render(request, "mentor/tsignup.html")

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, "mentor/tsignup.html")

        # Attempt to create the team
        try:
            team = Team.objects.create(team_name=team_name, email=email, password=password)
            return render(request, "mentor/tsignup_success.html", {"team_id": team.team_id})
        except IntegrityError:
            messages.error(request, "Team name or email already exists. Please choose a different one.")
            return render(request, "mentor/tsignup.html")

    return render(request, "mentor/tsignup.html")

# def ttasks(request):
#     tasks = Task.objects.all()  # Fetch all tasks from the database
#     return render(request, 'mentor/ttasks.html', {'tasks': tasks})
def ttasks(request):
    team_id = request.session.get('team_id')
    
    if not team_id:
        return render(request, 'mentor/ttasks.html', {'tasks': [], 'submissions': {}})
    
    try:
        mteam = Mteam.objects.get(team_id=team_id)
    except Mteam.DoesNotExist:
        return render(request, 'mentor/ttasks.html', {'tasks': [], 'submissions': {}})
    
    mentor_email = mteam.m_email
    tasks = Task.objects.filter(m_email=mentor_email)

   

    return render(request, 'mentor/ttasks.html', {
        'tasks': tasks,
        
    })

def upload_task_file(request, task_id):
    if request.method == 'POST' and request.FILES.get('file'):
        # Step 1: Retrieve team_id from the session
        team_id = request.session.get('team_id')
        if not team_id:
            return redirect('ttasks')  # Redirect if team_id is not in session

        # Step 2: Fetch the Team object to get team_name
        try:
            team = Team.objects.get(team_id=team_id)
        except Team.DoesNotExist:
            return redirect('ttasks')  # Redirect if team does not exist

        # Step 3: Fetch the Mteam object to get m_email
        try:
            mteam = Mteam.objects.get(team_id=team_id)
        except Mteam.DoesNotExist:
            return redirect('ttasks')  # Redirect if Mteam does not exist

        # Step 4: Fetch the Task object using task_id
        task = get_object_or_404(Task, task_id=task_id)

        # Step 5: Ensure the m_email in Task matches the m_email in Mteam
        if task.m_email != mteam.m_email:
            return redirect('ttasks')  # Redirect if m_email does not match

        # Step 6: Update the Task object with the uploaded file
        task.upload_file = request.FILES['file']
        task.save()

        # Step 7: Create a Ttask entry with the uploaded file and associated data
        Ttask.objects.create(
            task_id=task,  # Link to the Task object
            team_id=team,
            team_name=team.team_name,
            m_email=mteam.m_email,
            file_upload=request.FILES['file']
        )

        return redirect('ttasks')  # Redirect to task page after upload

    return redirect('ttasks')    # Redirect to task page after upload

    






def insertmentor(request):
    vuname=request.POST['tuname']
    vuemail=request.POST['tuemail']
    vucontact=request.POST['tucontact']
    vupassword=request.POST['tupassword']
    us=Signup(uname=vuname,uemail=vuemail,ucontact=vucontact,upassword=vupassword)
    us.save()
    return render(request, 'Mentor_frontend/login.html',{})


def coordinator_dashboard(request):
    # Optimize queries using select_related() and prefetch_related()
    teams = Mteam.objects.select_related("team_id", "m_email", "c_email").all()

    # Prefetch related objects to reduce queries
    project_lookup = {project.team_id.team_id: project.project_name for project in ProjectDetails.objects.all()}
    team_members_lookup = {}
    
    for member in TeamMember.objects.all():
        if member.team_id.team_id not in team_members_lookup:
            team_members_lookup[member.team_id.team_id] = []
        team_members_lookup[member.team_id.team_id].append(member.member_name)

    # Prepare the data structure
    data = []
    for team in teams:
        team_id = team.team_id.team_id  # Correct way to access foreign key
        project_name = project_lookup.get(team_id, "N/A")
        members = team_members_lookup.get(team_id, [])

        data.append({
            'team_id': team_id,
            'team_name': team.team_id.team_name,
            'project_name': project_name,
            'members': members
        })

    mentors = Mentor.objects.all()

    return render(request, "mentor/cdashboard.html", {
        "data": data,
        "mentors": mentors
    })