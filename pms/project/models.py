from django.db import models
from django.contrib.auth.hashers import make_password,check_password
# Create your models here.
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
class Signup(models.Model):
    uname=models.CharField(max_length=100)
    uemail = models.EmailField()
    ucontact = models.CharField(max_length=15)
    upassword=models.CharField(max_length=8)
 
    class Meta:
            db_table = 'signup'

class Team(models.Model):
    team_id = models.AutoField(primary_key=True)
    team_name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=25)
    email=models.EmailField(null=True,blank=True)
    class Meta:
        db_table = 'team'
     
      
    def __str__(self):
        return self.team_name

class Coordinator(models.Model):
    coord_name = models.CharField(max_length=20)
    c_email = models.EmailField(unique=True,primary_key=True)
    phone_no = models.BigIntegerField()
    password=models.CharField(max_length=25,null=True,blank=True)
    
    class Meta:
        db_table = 'coordinator'
        
    def __str__(self):
        return self.coord_name
    
class Mentor(models.Model):
    m_email = models.EmailField(primary_key=True)
    phone_no = models.BigIntegerField()
    mentor_name = models.CharField(max_length=20)
    password=models.CharField(max_length=25)

    class Meta:
        db_table = 'mentor'
        
    def __str__(self):
        return self.mentor_name
    
class TeamMember(models.Model):
    stu_id = models.CharField(max_length=30, primary_key=True)
    member_name = models.CharField(max_length=30)
    student_class = models.CharField(max_length=20)  # Changed "class" to avoid conflicts with Python keyword
    branch = models.CharField(max_length=30)
    semester = models.IntegerField()
    stu_rollno = models.IntegerField()
    phone_no = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',  # Ensures exactly 10 digits
                message="Phone number must be exactly 10 digits.",
                code="invalid_phone_number"
            )
        ]
    )
    email = models.CharField(max_length=50)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')  # Foreign key reference to Team

    class Meta:
        db_table = 'team_member'
    
    def __str__(self):
        return self.member_name
    def save(self, *args, **kwargs):
        # Count existing members in the team
        existing_members = TeamMember.objects.filter(team_id=self.team_id).count()

        if existing_members >= 5:
            raise ValidationError("A team cannot have more than 5 members.")

        super().save(*args, **kwargs)  # Save only if validation passes



# Group Details Model
class GroupDetails(models.Model):
    group_id = models.CharField(max_length=10, primary_key=True)
    mentor_name = models.CharField(max_length=20)
    project_name = models.CharField(max_length=20)
    m_email = models.ForeignKey(Mentor, on_delete=models.CASCADE)   # Mentor Email (Foreign Key Reference)
    c_email = models.ForeignKey(Coordinator, on_delete=models.CASCADE)  # Client Email (Foreign Key Reference)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE, db_column='team_id')     # Team ID (Foreign Key Reference)
    
    class Meta:
        db_table = 'group_details'

    def __str__(self):
        return self.group_id


# Marks Model
class Marks(models.Model):
    stu_rollno = models.CharField(max_length=20, primary_key=True)
    marks = models.IntegerField()
    member_name = models.CharField(max_length=30)
    stu_id = models.ForeignKey(TeamMember,on_delete=models.CASCADE)    # Student ID (Foreign Key Reference)
    c_email = models.ForeignKey(Coordinator, on_delete=models.CASCADE,null=True,blank=True) # Client Email (Foreign Key Reference)
    m_email = models.ForeignKey(Mentor, on_delete=models.CASCADE)  # Mentor Email (Foreign Key Reference)
    coordinator_marks=models.IntegerField(null=True,blank=True)
    percentage=models.IntegerField(null=True,blank=True)
    grade=models.CharField(max_length=10,null=True,blank=True)
    class Meta:
        db_table = 'marks'
    def __str__(self):
        return self.stu_rollno

# Project Details Model
class ProjectDetails(models.Model):
    project_id = models.AutoField(primary_key=True)
    description = models.TextField(max_length=200)
    project_name = models.CharField(max_length=30)
    approval = models.CharField(max_length=10,default='pending')
    tech_stack = models.TextField(max_length=100)
    team_id = models.CharField(max_length=10)   # Team ID (Foreign Key Reference)
    m_email = models.ForeignKey(Mentor, on_delete=models.CASCADE,null=True,blank=True)  # Mentor Email (Foreign Key Reference)
    c_email = models.ForeignKey(Coordinator, on_delete=models.CASCADE,null=True,blank=True)  # Client Email (Foreign Key Reference)

    class Meta:
        db_table = 'project_details'
    def __str__(self):
        return self.project_name



class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    doc_title = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    upload_file = models.FileField(upload_to='uploads/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(null=True)  # Add this field
    m_email = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    file_upload=models.FileField(upload_to='uploads/', null=True, blank=True)


    class Meta:
        db_table = 'task'
        
    def __str__(self):
        return self.doc_title
    
    
class Mteam(models.Model):
    team_id = models.OneToOneField(Team, on_delete=models.CASCADE, primary_key=True)
    m_email = models.ForeignKey(Mentor, null=True, blank=True, on_delete=models.CASCADE)
    c_email = models.ForeignKey(Coordinator, null=True, blank=True ,on_delete=models.CASCADE)

    class Meta:
        db_table = 'mteam'

    def __str__(self):
        return f"{self.team_id.team_name} - {self.m_email.name} - {self.c_email.name}"
    

class Mmentor(models.Model):
    m_email = models.OneToOneField(Mentor, on_delete=models.CASCADE, primary_key=True)
    phone_no = models.BigIntegerField()
    mentor_name = models.CharField(max_length=20)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)

    class Meta:
        db_table = 'mmentor'

    def __str__(self):
        return f"{self.mentor_name} - {self.team_id.team_name}"
    
class Ttask(models.Model):
    task_id = models.ForeignKey(Task,on_delete=models.CASCADE)
    Ttask_id=models.AutoField(primary_key=True)
    team_id=models.ForeignKey(Team, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=20)
    m_email = models.ForeignKey(Mentor, null=True, blank=True, on_delete=models.CASCADE)
    file_upload=models.FileField(upload_to='uploads/', null=True, blank=True)
    
    class Meta:
        db_table = 'Ttask'