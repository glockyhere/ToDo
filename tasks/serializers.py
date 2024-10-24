from rest_framework import serializers
from .models import Task, Comment
from datetime import date

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'status', 'due_date', 'created_at', 'updated_at', 'user']
        read_only_fields = ['id', 'created_at', 'updated_at', 'user']

    def validate_due_date(self, value):
        if value < date.today():
            raise serializers.ValidationError("Дата выполнения задачи не может быть в прошлом.")
        return value
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at', 'task', 'user']
        read_only_fields = ['id', 'created_at', 'user', 'task']

    def create(self, validated_data):
        request = self.context.get('request')
        return Comment.objects.create(user=request.user, **validated_data)