from django.urls import path, re_path

from .views import (
    CommentCount,
    CommentCreate,
    CommentList,
    CreateReportFlag,
    PostCommentReaction,
)

urlpatterns = [
    path("comment/", CommentCreate.as_view(), name="comments-ink-api-create"),
    re_path(
        r"^(?P<content_type>\w+[-]{1}\w+)/(?P<object_pk>[-\w]+)/$",
        CommentList.as_view(),
        name="comments-ink-api-list",
    ),
    re_path(
        r"^(?P<content_type>\w+[-]{1}\w+)/(?P<object_pk>[-\w]+)/count/$",
        CommentCount.as_view(),
        name="comments-ink-api-count",
    ),
    path(
        "react/",
        PostCommentReaction.as_view(),
        name="comments-ink-api-react",
    ),
    path("flag/", CreateReportFlag.as_view(), name="comments-ink-api-flag"),
]
