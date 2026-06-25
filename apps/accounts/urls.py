from django.urls import path

from .views import AccountLogoutView, ApprovedLoginView, AwaitingApprovalView, SignupView

app_name = 'accounts'

urlpatterns = [
    path('login/', ApprovedLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('awaiting-approval/', AwaitingApprovalView.as_view(), name='awaiting_approval'),
]
