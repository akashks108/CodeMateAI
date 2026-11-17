from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .services import execute_code
from .ai_service import generate_lesson, generate_practice_question
from .models import Language, Topic, StudentLanguageProgress


@login_required(login_url='login')
def student_dashboard(request):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    return render(request, 'student/dashboard.html')

# This view loads the selected programming language and remembers the student's current learning topic.
@login_required(login_url='login')
def learning_page(request, language):
    if request.user.is_superuser:
        return redirect('admin_dashboard')

    if language not in ['python', 'java', 'c', 'cpp', 'php']:
        return redirect('student_dashboard')

    selected_language = Language.objects.filter(
        slug=language
    ).first()

    levels = []
    current_topic = None

    if selected_language:
        levels = selected_language.levels.prefetch_related(
            'topics'
        ).all()

        first_topic = Topic.objects.filter(
            level__language=selected_language
        ).order_by(
            'level__order',
            'order'
        ).first()

        progress, created = StudentLanguageProgress.objects.get_or_create(
            student=request.user,
            language=selected_language,
            defaults={'current_topic': first_topic}
        )

        current_topic = progress.current_topic

        if current_topic is None:
            current_topic = first_topic
            progress.current_topic = current_topic
            progress.save(update_fields=['current_topic', 'updated_at'])

    return render(request, 'student/learning.html', {
        'language': language,
        'levels': levels,
        'current_topic': current_topic
    })
    
# Save the student's selected topic as their current learning position for that language.
@login_required(login_url='login')
@require_POST
def save_current_topic(request):

    if request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'error': 'Access denied.'
        }, status=403)

    try:
        data = json.loads(request.body)
        topic_id = data.get('topic_id')

        if not topic_id:
            return JsonResponse({
                'status': 'error',
                'error': 'Topic ID is required.'
            }, status=400)

        topic = Topic.objects.select_related(
            'level__language'
        ).get(id=topic_id)

        progress, created = StudentLanguageProgress.objects.get_or_create(
            student=request.user,
            language=topic.level.language
        )

        progress.current_topic = topic
        progress.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Current topic saved successfully.'
        })

    except (json.JSONDecodeError, TypeError):
        return JsonResponse({
            'status': 'error',
            'error': 'Invalid request data.'
        }, status=400)

    except Topic.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'error': 'Selected topic does not exist.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
    
@login_required(login_url='login')
@require_POST
def run_code(request):
    if request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'error': 'Access denied.'
        }, status=403)

    try:
        data = json.loads(request.body)

        language = data.get('language', '')
        code = data.get('code', '')
        user_input = data.get('input', '')

        if language not in ['python', 'java', 'c', 'cpp', 'php']:
            return JsonResponse({
                'status': 'error',
                'error': 'Unsupported programming language.'
            }, status=400)

        if not isinstance(code, str) or not code.strip():
            return JsonResponse({
                'status': 'error',
                'error': 'Please write some code before running.'
            }, status=400)

        if len(code) > 20000 or not isinstance(user_input, str) or len(user_input) > 10000:
            return JsonResponse({
                'status': 'error',
                'error': 'Code or input exceeds the allowed size.'
            }, status=400)

        result = execute_code(language, code, user_input)

        return JsonResponse(result)

    except (json.JSONDecodeError, UnicodeDecodeError, AttributeError):
        return JsonResponse({
            'status': 'error',
            'error': 'Invalid request data.'
        }, status=400)
        
# Generate an AI lesson for the selected curriculum topic
@login_required(login_url='login')
@require_POST
def generate_ai_lesson(request):

    if request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'error': 'Access denied.'
        }, status=403)

    try:
        data = json.loads(request.body)
        topic_id = data.get('topic_id')

        topic = Topic.objects.select_related(
            'level__language'
        ).get(id=topic_id)

        lesson = generate_lesson(
            language=topic.level.language.name,
            level=topic.level.name,
            topic=topic.title,
            description=topic.description
        )

        return JsonResponse({
            'status': 'success',
            'lesson': lesson
        })

    except Topic.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'error': 'Selected topic does not exist.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)
        
# Generate another practice question for the selected topic
@login_required(login_url='login')
@require_POST
def generate_next_practice(request):

    if request.user.is_superuser:
        return JsonResponse({
            'status': 'error',
            'error': 'Access denied.'
        }, status=403)

    try:
        data = json.loads(request.body)
        topic_id = data.get('topic_id')

        topic = Topic.objects.select_related(
            'level__language'
        ).get(id=topic_id)

        question = generate_practice_question(
            language=topic.level.language.name,
            level=topic.level.name,
            topic=topic.title,
            description=topic.description
        )

        return JsonResponse({
            'status': 'success',
            'question': question
        })

    except Topic.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'error': 'Selected topic does not exist.'
        }, status=404)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'error': str(e)
        }, status=500)