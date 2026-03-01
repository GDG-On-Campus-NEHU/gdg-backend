from django.db import migrations
from django.utils.text import slugify


def _generate_unique_slug(model_cls, base_value, instance_pk=None, default_prefix='item'):
    base_slug = slugify(base_value) or default_prefix
    candidate = base_slug
    suffix = 1
    while model_cls.objects.exclude(pk=instance_pk).filter(slug=candidate).exists():
        candidate = f"{base_slug}-{suffix}"
        suffix += 1
    return candidate


def backfill_slugs(apps, schema_editor):
    model_configs = [
        ('BlogPost', 'title', 'blog'),
        ('Project', 'title', 'project'),
        ('Event', 'title', 'event'),
        ('Roadmap', 'title', 'roadmap'),
        ('TeamMember', 'name', 'member'),
    ]

    for model_name, source_field, default_prefix in model_configs:
        model_cls = apps.get_model('landing_page', model_name)
        for instance in model_cls.objects.all().iterator():
            if instance.slug:
                continue
            source_value = getattr(instance, source_field, '')
            instance.slug = _generate_unique_slug(
                model_cls,
                source_value,
                instance_pk=instance.pk,
                default_prefix=default_prefix,
            )
            instance.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('landing_page', '0016_blogpost_slug_event_slug_project_slug_roadmap_slug_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_slugs, migrations.RunPython.noop),
    ]
