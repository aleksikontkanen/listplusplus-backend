from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TaskList, ListItem


class UserSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    task_lists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=TaskList.objects.all()
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'task_lists'
        )


class ListItemSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    owners = UserSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = ListItem
        fields = (
            'id',
            'name',
            'state',
            'owners',
            'date_created',
            'date_modified'
        )
        read_only_fields = (
            'owner',
            'date_created',
            'date_modified'
        )


class TaskListSerializer(serializers.ModelSerializer):
    """Serializer to map the Model instance into JSON format."""

    owners = UserSerializer(many=True, read_only=True)
    list_items = ListItemSerializer(many=True, read_only=True)

    class Meta:
        """Meta class to map serializer's fields with the model fields."""
        model = TaskList
        fields = (
            'id',
            'owners',
            'name',
            'list_items',
            'date_created',
            'date_modified'
        )
        read_only_fields = (
            'owners',
            'list_items',
            'date_created',
            'date_modified'
        )
