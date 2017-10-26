from django.conf.urls import url, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserList, UserDetail, TaskListList, TaskListDetail, TaskListShare, ListItemList, ListItemDetail, api_root

urlpatterns = {
    url(r'^api/v1/authenticate/', obtain_auth_token, name="api_auth"),
    url(r'^api/v1/$', api_root, name="api_root"),
    url(r'^api/v1/users/$', UserList.as_view(), name="user_list"),
    url(r'^api/v1/users/(?P<pk>[0-9]+)/$',
        UserDetail.as_view(), name="user_details"),
    url(r'^api/v1/tasklists/$', TaskListList.as_view(), name="task_list_create"),
    url(r'^api/v1/tasklists/(?P<pk>[0-9]+)/$',
        TaskListDetail.as_view(), name="task_list_details"),
    url(r'^api/v1/tasklists_share/$',
        TaskListShare.as_view(), name="task_list_share"),
    url(r'^api/v1/listitems/$', ListItemList.as_view(), name="list_item_create"),
    url(r'^api/v1/listitems/(?P<pk>[0-9]+)/$',
        ListItemDetail.as_view(), name="list_item_details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)
