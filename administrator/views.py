from django.views.decorators.http import require_POST
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import get_user_model
from django.contrib import messages

from student.models import Language, Level, Topic
from django.db.models import Max

def is_admin(user):
    return user.is_authenticated and user.is_superuser


@user_passes_test(is_admin, login_url='login')
def admin_dashboard(request):
    User = get_user_model()

    total_students = User.objects.filter(
        is_superuser=False,
        is_staff=False
    ).count()

    return render(request, 'administrator/dashboard.html', {
        'total_students': total_students
    })
@user_passes_test(is_admin, login_url='login')
def student_list(request):
    User = get_user_model()

    students = User.objects.filter(
        is_superuser=False,
        is_staff=False
    ).order_by('-date_joined')

    return render(request, 'administrator/students.html', {
        'students': students
    })
    
@user_passes_test(is_admin, login_url='login')
def curriculum_management(request):

    languages = Language.objects.all().order_by('name')

    selected_language = None

    language_slug = request.GET.get('language')

    if language_slug:
        selected_language = get_object_or_404(
            Language,
            slug=language_slug
        )

    return render(request, 'administrator/curriculum.html', {
        'languages': languages,
        'selected_language': selected_language,
        'active_page': 'curriculum'
    })
    
@user_passes_test(is_admin, login_url='login')
def add_topic(request, language_slug, level_id):

    level = get_object_or_404(
        Level,
        id=level_id,
        language__slug=language_slug
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()

        if not title:
            return render(request, 'administrator/add_topic.html', {
                'level': level,
                'error': 'Topic title is required.'
            })

        last_order = Topic.objects.filter(
            level=level
        ).aggregate(max_order=Max('order'))['max_order'] or 0

        Topic.objects.create(
            level=level,
            title=title,
            description=description,
            order=last_order + 1
        )

        messages.success(request, 'Topic added successfully.')

        return redirect(
            f"/admin-dashboard/curriculum/?language={language_slug}"
        )

    return render(request, 'administrator/add_topic.html', {
        'level': level
    })

@user_passes_test(is_admin, login_url='login')
def edit_topic(request, language_slug, topic_id):

    topic = get_object_or_404(
        Topic,
        id=topic_id,
        level__language__slug=language_slug
    )

    if request.method == 'POST':

        title = request.POST.get('title', '').strip()

        if not title:
            return render(request, 'administrator/edit_topic.html', {
                'topic': topic,
                'error': 'Topic title is required.'
            })

        topic.title = title
        topic.save()

        messages.success(request, 'Topic updated successfully.')

        return redirect(
            f"/admin-dashboard/curriculum/?language={language_slug}"
        )

    return render(request, 'administrator/edit_topic.html', {
        'topic': topic
    })

@user_passes_test(is_admin, login_url='login')
@require_POST
def delete_topic(request, language_slug, topic_id):

    topic = get_object_or_404(
        Topic,
        id=topic_id,
        level__language__slug=language_slug
    )

    topic.delete()

    messages.success(request, 'Topic deleted successfully.')

    return redirect(
        f"/admin-dashboard/curriculum/?language={language_slug}"
    )