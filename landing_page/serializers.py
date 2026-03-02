from django.utils import timezone
from rest_framework import serializers

from .models import (
    Tag,
    Project,
    ProjectContributor,
    BlogPost,
    TeamMember,
    Roadmap,
    Event,
    Speaker,
    EventResource,
)


class BasicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color']


class TagSerializer(BasicTagSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta(BasicTagSerializer.Meta):
        fields = BasicTagSerializer.Meta.fields + ['count']


class TaggableSerializerMixin:
    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        instance = super().create(validated_data)
        if tags:
            instance.tags.set(tags)
        return instance

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        instance = super().update(instance, validated_data)
        if tags is not None:
            instance.tags.set(tags)
        return instance


class ProjectContributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectContributor
        fields = [
            'id',
            'name',
            'role_type',
            'photo_url',
            'github_url',
            'linkedin_url',
            'website_url',
            'order',
        ]
        read_only_fields = ['id']


class ProjectBaseSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )
    contributors = ProjectContributorSerializer(many=True, required=False)

    class Meta:
        model = Project
        fields = [
            'id',
            'slug',
            'title',
            'description',
            'image_url',
            'is_open_source',
            'status',
            'repo_url',
            'demo_url',
            'tags',
            'tag_ids',
            'author_name',
            'published_date',
        ]

    def _replace_contributors(self, project, contributors_data):
        if contributors_data is None:
            return
        project.contributors.all().delete()
        for index, payload in enumerate(contributors_data):
            defaults = {
                'name': payload.get('name', '').strip(),
                'role_type': payload.get('role_type', '').strip(),
                'photo_url': payload.get('photo_url', ''),
                'github_url': payload.get('github_url', ''),
                'linkedin_url': payload.get('linkedin_url', ''),
                'website_url': payload.get('website_url', ''),
                'order': payload.get('order', index + 1),
            }
            ProjectContributor.objects.create(project=project, **defaults)

    def create(self, validated_data):
        contributors_data = validated_data.pop('contributors', [])
        project = super().create(validated_data)
        self._replace_contributors(project, contributors_data)
        return project

    def update(self, instance, validated_data):
        contributors_data = validated_data.pop('contributors', None)
        project = super().update(instance, validated_data)
        if contributors_data is not None:
            self._replace_contributors(project, contributors_data)
        return project


class ProjectListSerializer(ProjectBaseSerializer):
    pass


class ProjectDetailSerializer(ProjectBaseSerializer):
    class Meta(ProjectBaseSerializer.Meta):
        fields = ProjectBaseSerializer.Meta.fields + ['content', 'contributors']


class BlogPostBaseSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )

    class Meta:
        model = BlogPost
        fields = ['id', 'slug', 'title', 'summary', 'image_url', 'tags', 'tag_ids', 'author_name', 'published_date']


class BlogPostListSerializer(BlogPostBaseSerializer):
    pass


class BlogPostDetailSerializer(BlogPostBaseSerializer):
    class Meta(BlogPostBaseSerializer.Meta):
        fields = BlogPostBaseSerializer.Meta.fields + ['content']


class TeamMemberBaseSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = [
            'id',
            'slug',
            'name',
            'role',
            'photo_url',
            'skills',
            'skills_list',
            'tags',
            'tag_ids',
            'position_rank',
            'github_url',
            'linkedin_url',
            'instagram_url',
            'twitter_url',
            'website_url',
        ]

    def get_skills_list(self, obj):
        if obj.skills:
            return [skill.strip() for skill in obj.skills.split(',') if skill.strip()]
        return []


class TeamMemberListSerializer(TeamMemberBaseSerializer):
    pass


class TeamMemberDetailSerializer(TeamMemberBaseSerializer):
    class Meta(TeamMemberBaseSerializer.Meta):
        fields = TeamMemberBaseSerializer.Meta.fields + ['bio']


class RoadmapBaseSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )

    class Meta:
        model = Roadmap
        fields = ['id', 'slug', 'icon_name', 'title', 'description', 'tags', 'tag_ids', 'author_name', 'published_date']


class RoadmapListSerializer(RoadmapBaseSerializer):
    pass


class RoadmapDetailSerializer(RoadmapBaseSerializer):
    class Meta(RoadmapBaseSerializer.Meta):
        fields = RoadmapBaseSerializer.Meta.fields + ['content']


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name', 'profile_image', 'bio', 'social_link']


class EventResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventResource
        fields = ['label', 'url']


class EventBaseSerializer(TaggableSerializerMixin, serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )
    speakers = SpeakerSerializer(many=True, read_only=True)
    tech_tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name',
        source='tech_tag_items',
    )
    gallery_images = serializers.SerializerMethodField()
    resources = EventResourceSerializer(many=True, read_only=True, source='resource_items')
    registration_open = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id',
            'slug',
            'title',
            'summary',
            'image_url',
            'tags',
            'tag_ids',
            'author_name',
            'event_date',
            'requires_registration',
            'registration_link',
            'registration_deadline',
            'registration_open',
            'mode',
            'location_address',
            'meeting_link',
            'tech_tags',
            'speakers',
            'gallery_images',
            'resources',
        ]

    def get_gallery_images(self, obj):
        return [image.image_url for image in obj.gallery_image_items.all()]

    def get_registration_open(self, obj):
        if not obj.requires_registration:
            return False
        if not obj.registration_deadline:
            return bool(obj.registration_link)
        return timezone.now() <= obj.registration_deadline


class EventListSerializer(EventBaseSerializer):
    pass


class EventDetailSerializer(EventBaseSerializer):
    class Meta(EventBaseSerializer.Meta):
        fields = EventBaseSerializer.Meta.fields + ['content']


# Backward-compatible aliases used in aggregate endpoints.
class ProjectSerializer(ProjectDetailSerializer):
    pass


class BlogPostSerializer(BlogPostDetailSerializer):
    pass


class TeamMemberSerializer(TeamMemberDetailSerializer):
    pass


class RoadmapSerializer(RoadmapDetailSerializer):
    pass


class EventSerializer(EventDetailSerializer):
    pass


class UnifiedItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    title = serializers.CharField()
    summary = serializers.CharField(allow_blank=True)
    image_url = serializers.CharField(allow_blank=True)
    tags = BasicTagSerializer(many=True)
