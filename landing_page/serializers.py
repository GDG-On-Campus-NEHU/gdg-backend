from rest_framework import serializers
from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event, Speaker


class BasicTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'color']


class TagSerializer(BasicTagSerializer):
    count = serializers.IntegerField(read_only=True)

    class Meta(BasicTagSerializer.Meta):
        fields = BasicTagSerializer.Meta.fields + ['count']


class ProjectSerializer(serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'content', 'image_url', 'tags', 'tag_ids', 'author_name', 'published_date']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        project = super().create(validated_data)
        if tags:
            project.tags.set(tags)
        return project

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        project = super().update(instance, validated_data)
        if tags is not None:
            project.tags.set(tags)
        return project


class BlogPostSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'title', 'summary', 'content', 'image_url', 'tags', 'tag_ids', 'author_name', 'published_date']

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        blog = super().create(validated_data)
        if tags:
            blog.tags.set(tags)
        return blog

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        blog = super().update(instance, validated_data)
        if tags is not None:
            blog.tags.set(tags)
        return blog


class TeamMemberSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'name', 'role', 'photo_url', 'bio', 'skills', 'skills_list',
                  'tags', 'tag_ids', 'position_rank', 'github_url', 'linkedin_url',
                  'instagram_url', 'twitter_url', 'website_url']

    def get_skills_list(self, obj):
        if obj.skills:
            return [skill.strip() for skill in obj.skills.split(',') if skill.strip()]
        return []


class RoadmapSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'icon_name', 'title', 'description', 'content', 'tags', 'tag_ids', 'author_name', 'published_date']


class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = ['name', 'profile_image', 'bio', 'social_link']


class EventSerializer(serializers.ModelSerializer):
    tags = BasicTagSerializer(many=True, read_only=True)
    speakers = SpeakerSerializer(many=True, read_only=True)
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all(),
        write_only=True,
        source='tags',
        required=False,
    )

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'summary', 'content', 'image_url', 'tags', 'tag_ids', 'author_name', 'event_date',
            'requires_registration', 'registration_link', 'mode', 'location_address', 'meeting_link',
            'tech_tags', 'speakers', 'gallery_images'
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['tech_tags'] = data.get('tech_tags') or []
        data['gallery_images'] = data.get('gallery_images') or []
        return data


class UnifiedItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    title = serializers.CharField()
    summary = serializers.CharField(allow_blank=True)
    image_url = serializers.CharField(allow_blank=True)
    tags = BasicTagSerializer(many=True)
