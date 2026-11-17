
import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from student.models import Language, Level, Topic


class Command(BaseCommand):
    help = "Import programming curricula from JSON file"

    def handle(self, *args, **options):

        file_path = (
            Path(__file__).resolve().parents[2]
            / "data"
            / "curriculum.json"
        )

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                curriculum = json.load(file)
        except FileNotFoundError:
            raise CommandError("Curriculum JSON file not found.")
        except json.JSONDecodeError as error:
            raise CommandError(f"Invalid JSON file: {error}")

        for language_data in curriculum["languages"]:

            language, created = Language.objects.get_or_create(
                slug=language_data["slug"],
                defaults={"name": language_data["language"]}
            )

            if created:
                self.stdout.write(f"Created language: {language.name}")

            for level_data in language_data["levels"]:

                level, created = Level.objects.get_or_create(
                    language=language,
                    order=level_data["order"],
                    defaults={"name": level_data["name"]}
                )

                if created:
                    self.stdout.write(f"Created level: {level.name}")

                for topic_order, topic_title in enumerate(
                    level_data["topics"], start=1
                ):

                    topic, created = Topic.objects.get_or_create(
                        level=level,
                        order=topic_order,
                        defaults={"title": topic_title}
                    )

                    if created:
                        self.stdout.write(
                            f"Added topic: {topic.title}"
                        )

            total_topics = Topic.objects.filter(
                level__language=language
            ).count()

            self.stdout.write(
                f"{language.name}: {total_topics} topics imported."
            )

        self.stdout.write(
            self.style.SUCCESS(
                "All curriculum imports completed successfully!"
            )
        )
