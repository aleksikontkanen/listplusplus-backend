from rest_framework import status, permissions
from rest_framework.generics import ListAPIView, RetrieveAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.views import APIView
from .serializers import UserSerializer, TaskListSerializer, ListItemSerializer
from .permissions import IsOwner
from django.contrib.auth.models import User
from .models import TaskList, ListItem
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# API entry point

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'authentication': reverse('api_auth', request=request, format=format),
        'users': reverse('user_list', request=request, format=format),
        'tasklists': reverse('task_list_create', request=request, format=format),
        'tasklist_share': reverse('task_list_share', request=request, format=format),
        'listitems': reverse('list_item_create', request=request, format=format)
    })


# Users

class UserList(ListAPIView):
    """List all users."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(RetrieveAPIView):
    """Retrieve a user."""

    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# Task lists

@method_decorator(csrf_exempt, name='dispatch')
class TaskListList(ListCreateAPIView):
    """List all task lists, or create a new task list."""

    permission_classes = (IsOwner,)
    serializer_class = TaskListSerializer

    def get_queryset(self):
        taskLists = TaskList.objects.all()
        results = []

        for taskList in taskLists:
            if self.request.user in taskList.owners.all():
                results.append(taskList)

        return results

    def perform_create(self, serializer):
        serializer.save(owners=[self.request.user])


@method_decorator(csrf_exempt, name='dispatch')
class TaskListDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a list."""

    permission_classes = (IsOwner,)
    queryset = TaskList.objects.all()
    serializer_class = TaskListSerializer


@method_decorator(csrf_exempt, name='dispatch')
class TaskListShare(APIView):
    """Share a list with multiple users"""

    def post(self, request, format=None):
        requester = self.request.user
        taskListId = self.request.data.get('tasklist_id', None)
        userEmail = self.request.data.get('share_to_email', None)

        userToShare = User.objects.get(email=userEmail)
        taskList = TaskList.objects.get(pk=taskListId)

        if userEmail is not None and taskListId is not None:
            if requester in taskList.owners.all() and userToShare not in taskList.owners.all():
                taskList.owners.add(userToShare)
                taskList.save()

            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# List items

@method_decorator(csrf_exempt, name='dispatch')
class ListItemList(ListCreateAPIView):
    """List all list items, or create a new list item."""

    permission_classes = (IsOwner,)
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer

    def perform_create(self, serializer):
        serializer.save(
            owners=[self.request.user],
            task_list=TaskList.objects.get(
                pk=self.request.data.get('task_list_id'))
        )


@method_decorator(csrf_exempt, name='dispatch')
class ListItemDetail(RetrieveUpdateDestroyAPIView):
    """Retrieve, update or delete a list."""

    permission_classes = (IsOwner,)
    queryset = ListItem.objects.all()
    serializer_class = ListItemSerializer
