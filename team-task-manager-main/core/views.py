from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json

from django.contrib.auth import get_user_model
User = get_user_model()

from .models import Project, Task
from .serializers import RegisterSerializer


# ✅ REGISTER
@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User created"}, status=201)
    return Response(serializer.errors, status=400)


# ✅ LOGIN
@csrf_exempt
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "Invalid credentials"})

        user = authenticate(
            username=user_obj.username,
            password=password
        )

        if user:
            login(request, user)
            return redirect("/dashboard/")

        return render(request, "login.html", {"error": "Invalid credentials"})

    return render(request, "login.html")


# ✅ PAGES
def login_page(request):
    return render(request, 'login.html')


def signup_page(request):
    return render(request, 'signup.html')


# ✅ DASHBOARD
@login_required
def dashboard(request):
    tasks = Task.objects.filter(assigned_to=request.user)

    overdue = tasks.filter(
        due_date__lt=timezone.now(),
        status__in=["todo", "in_progress"]
    ).count()

    context = {
        "tasks": tasks[:5],
        "total_tasks": tasks.count(),
        "completed": tasks.filter(status="done").count(),
        "pending": tasks.filter(status="todo").count(),
        "overdue": overdue,
        "total_projects": Project.objects.filter(members=request.user).count(),
    }

    return render(request, "dashboard.html", context)


# ✅ PROJECT LIST
@login_required
def projects_page(request):
    projects = Project.objects.filter(members=request.user)

    for project in projects:
        total = project.tasks.count()
        done = project.tasks.filter(status="done").count()
        project.progress = int((done / total) * 100) if total > 0 else 0

    return render(request, "projects.html", {"projects": projects})


# ✅ PROJECT DETAIL
@login_required
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)

    # ✅ अगर member नहीं है → add कर दो (TEMP FIX)
    if request.user not in project.members.all():
        project.members.add(request.user)

    tasks = project.tasks.all()

    return render(request, "project_detail.html", {
        "project": project,
        "tasks": tasks
    })

# ✅ CREATE PROJECT
@csrf_exempt
@login_required
def create_project(request):
    if request.method == "POST":
        data = json.loads(request.body)

        project = Project.objects.create(
            name=data.get("name"),
            created_by=request.user
        )

        project.members.add(request.user)
        project.admins.add(request.user)  # ✅ MUST

        return JsonResponse({"message": "created"}, status=201)
# ✅ DELETE PROJECT (ADMIN ONLY)
@csrf_exempt
@login_required
def delete_project(request, id):
    if request.method == "POST":
        project = get_object_or_404(Project, id=id)

        if request.user not in project.admins.all():
            return JsonResponse({"error": "Not allowed"}, status=403)

        project.delete()
        return JsonResponse({"message": "deleted"}, status=200)
# ✅ ADD MEMBER (ADMIN ONLY)
@csrf_exempt
@login_required
def add_member(request, id):
    if request.method == "POST":
        data = json.loads(request.body)

        project = get_object_or_404(Project, id=id)

        # ✅ ONLY ADMIN CAN ADD
        if request.user not in project.admins.all():
            return JsonResponse({"error": "Only admin can add"}, status=403)

        try:
            user = User.objects.get(email=data.get("email"))
            project.members.add(user)
            return JsonResponse({"message": "member added"}, status=200)
        except User.DoesNotExist:
            return JsonResponse({"error": "user not found"}, status=404)
# ✅ ADD TASK
@csrf_exempt
@login_required
def add_task(request, id):
    if request.method == "POST":
        data = json.loads(request.body)

        project = get_object_or_404(Project, id=id, members=request.user)

        title = data.get("title")
        user_id = data.get("user_id")
        due_date = data.get("due_date")

        if not title:
            return JsonResponse({"error": "Title required"}, status=400)

        user = get_object_or_404(User, id=user_id)

        if user not in project.members.all():
            return JsonResponse({"error": "User not in project"}, status=400)

        # ✅ SAFE DATE FIX
        if not due_date:
            due_date = None

        Task.objects.create(
            title=title,
            project=project,
            assigned_to=user,
            status="todo",
            priority=data.get("priority", "medium"),
            due_date=due_date
        )

        return JsonResponse({"message": "created"}, status=201)


# ✅ DELETE TASK
@csrf_exempt
@login_required
def delete_task(request, id):
    if request.method == "POST":
        task = get_object_or_404(Task, id=id, project__members=request.user)

        if request.user not in task.project.members.all():
         return JsonResponse({"error": "Not allowed"}, status=403)

        task.delete()
        return JsonResponse({"message": "deleted"}, status=200)


# ✅ UPDATE TASK
# ✅ UPDATE TASK (FIXED)
@csrf_exempt
@login_required
def update_task_status(request, id):
    if request.method == "POST":
        data = json.loads(request.body)

        task = get_object_or_404(Task, id=id)

        # ✅ allow project members
        if request.user not in task.project.members.all():
            return JsonResponse({"error": "Not allowed"}, status=403)

        status = data.get("status")

        if status not in ["todo", "in_progress", "done"]:
            return JsonResponse({"error": "Invalid status"}, status=400)

        task.status = status
        task.save()

        return JsonResponse({"message": "updated", "status": task.status}, status=200)


# ✅ API TEST
def home(request):
    return JsonResponse({"message": "API working 🚀"})