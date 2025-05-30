from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Feedback
from .forms import FeedbackForm

# ✅ CBV: Create Feedback
class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('thank_you')

# ✅ CBV: List All Feedbacks
class FeedbackListView(ListView):
    model = Feedback
    template_name = 'feedback_list.html'
    context_object_name = 'feedbacks'
    ordering = ['-created_at']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['feedback_count'] = self.get_queryset().count()
        return context

# ✅ FBV: Thank You
def thank_you(request):
    return render(request, 'thank_you.html')

# ✅ CBV: Edit Feedback
class FeedbackUpdateView(UpdateView):
    model = Feedback
    form_class = FeedbackForm
    template_name = 'edit_feedback.html'
    success_url = reverse_lazy('feedback_list')

# ✅ CBV: Delete Feedback
class FeedbackDeleteView(DeleteView):
    model = Feedback
    template_name = 'confirm_delete.html'  # ✅ Make sure this template exists
    success_url = reverse_lazy('feedback_list')
