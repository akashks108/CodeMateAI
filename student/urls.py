from django.urls import path
# Import the views used for code execution, AI lessons, practice questions and learning progress.
from .views import (run_code,generate_ai_lesson,generate_next_practice,save_current_topic)


urlpatterns = [
    path('run-code/', run_code, name='run_code'),
    path('generate-lesson/', generate_ai_lesson, name='generate_ai_lesson'),
    path('next-practice/', generate_next_practice, name='generate_next_practice'),
    # Save the student's currently selected learning topic.
    path('save-current-topic/', save_current_topic, name='save_current_topic'),
]