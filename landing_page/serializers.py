from rest_framework import serializers
from .models import Tag, Project, BlogPost, TeamMember, Roadmap, Event

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['name']

class ProjectSerializer(serializers.ModelSerializer):
    # Readable tags for UI
    tags = TagSerializer(many=True, read_only=True)
    # Write-only tag IDs for API clients
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
        # Handle many-to-many tags
        tags = validated_data.pop('tags', [])
        project = super().create(validated_data)
        if tags:
            project.tags.set(tags)
        return project

    def update(self, instance, validated_data):
        # Allow tag updates when provided
        tags = validated_data.pop('tags', None)
        project = super().update(instance, validated_data)
        if tags is not None:
            project.tags.set(tags)
        return project

class BlogPostSerializer(serializers.ModelSerializer):
    # Readable tags for UI
    tags = TagSerializer(many=True, read_only=True)
    # Write-only tag IDs for API clients
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
        # Handle many-to-many tags
        tags = validated_data.pop('tags', [])
        blog = super().create(validated_data)
        if tags:
            blog.tags.set(tags)
        return blog

    def update(self, instance, validated_data):
        # Allow tag updates when provided
        tags = validated_data.pop('tags', None)
        blog = super().update(instance, validated_data)
        if tags is not None:
            blog.tags.set(tags)
        return blog

class TeamMemberSerializer(serializers.ModelSerializer):
    # Provide a computed list of skills for UI chips/badges
    skills_list = serializers.SerializerMethodField()

    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'role', 'photo_url', 'bio', 'skills', 'skills_list',
                  'position_rank', 'github_url', 'linkedin_url', 'instagram_url',
                  'twitter_url', 'website_url']

    def get_skills_list(self, obj):
        """Convert comma-separated skills string to list for frontend"""
        if obj.skills:
            return [skill.strip() for skill in obj.skills.split(',') if skill.strip()]
        return []

class RoadmapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roadmap
        fields = ['id', 'icon_name', 'title', 'description', 'content', 'author_name', 'published_date']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'summary', 'content', 'image_url', 'author_name', 'event_date']

