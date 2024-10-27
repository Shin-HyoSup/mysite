from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic

from .models import Question, Choice

# Create your views here.
class IndexView(generic.ListView):
    template_name='polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DeleteView):
    model = Question
    template_name = 'polls/result.html'

def index(request):
    #output = ', '.join([q.question_text for q in latest_question_list])
    #return HttpResponse(output)

    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    #1
    # templete = loader.get_template('polls/index.html')
    # context = {
    #     'latest_question_list' : latest_question_list,
    # }
    #return HttpResponse(templete.render(context, request))

    #2
    context = {'latest_question_list' : latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    #1
    #return HttpResponse("You're looking at question %s" % question_id)

    #2
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    
    # return render(request, 'polls/detail.html', {'question':question})

    #3
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question':question})


def results(request, question_id):
    #1
    # response = "You're looking at the results of question %s"
    # return HttpResponse(response % question_id)
    #2
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question':question})

def vote(request, question_id):
    # return HttpResponse("You're voting on question %s" % question_id)
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        #redisplay the question voting form.
        return render(request, 'polls/detail.html', {'question':question, 'error_message':"You didn't select a choice",})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))