
from django.db import models
from django.conf import settings

class Language(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Level(models.Model):
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='levels'
    )
    name = models.CharField(max_length=50)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('language', 'order')

    def __str__(self):
        return f"{self.language.name} - {self.name}"


class Topic(models.Model):
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='topics'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']
        unique_together = ('level', 'order')

    def __str__(self):
        return self.title

class StudentLanguageProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='language_progress'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )
    current_topic = models.ForeignKey(
        Topic,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='current_for_students'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'language')

    def __str__(self):
        return f"{self.student} - {self.language}"


class StudentTopicProgress(models.Model):
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='topic_progress'
    )
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='student_progress'
    )
    is_completed = models.BooleanField(default=False)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student} - {self.topic.title}"