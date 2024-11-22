from rest_framework import serializers

from users.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('title','description','assigned_user_id','status','due_date')
        
