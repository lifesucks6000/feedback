from django.urls import path
from .views import (
    FeedbackCreateView,
    FeedbackListView,
    FeedbackUpdateView,
    FeedbackDeleteView,
    thank_you,
)

urlpatterns = [
    path('', FeedbackCreateView.as_view(), name='feedback_form'),             # Create
    path('thank-you/', thank_you, name='thank_you'),                          # Thank You
    path('all/', FeedbackListView.as_view(), name='feedback_list'),           # Read
    path('edit/<int:pk>/', FeedbackUpdateView.as_view(), name='edit_feedback'), # Update
    path('delete/<int:pk>/', FeedbackDeleteView.as_view(), name='delete_feedback'), # Delete
]
