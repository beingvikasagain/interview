from django.shortcuts import render
from rest_framework.response import Response

# Create your views here.
from rest_framework.views import APIView

from users.models import Task
from users.serializers import TaskSerializer


class TaskView(APIView):
    def get(self, request):
        try:
            if 'status' in request.query_params:
                status = request.query_params.get('status')
                if status is not None and status in ('pending','completed'):
                    tasks = Task.objects.filter(status=status)
            else:
                tasks = Task.objects.all()
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            for each_field in ('title','description','assigned_user_id','status','due_date'):
                if each_field not in data:
                    return Response({"error": f"{each_field} field is required"}, status=400)
            task = Task(**data)
            task.save()
            return Response(task.id, status=201)
            
        except Exception as e:
            return Response({"error": str(e)}, status=500)

