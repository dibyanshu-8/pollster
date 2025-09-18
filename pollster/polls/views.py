# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from .models import Poll, Choice, Vote
from .forms import PollAddForm, EditPollForm, ChoiceAddForm
from django.http import HttpResponse, HttpResponseBadRequest


@login_required()
def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = ''

    # MODIFIED: Changed to elif to prevent sorts from overwriting each other.
    if 'name' in request.GET:
        all_polls = all_polls.order_by('text')
    elif 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')
    elif 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    # This logic preserves search/sort queries across different pages.
    get_dict_copy = request.GET.copy()
    if 'page' in get_dict_copy:
        del get_dict_copy['page']
    params = get_dict_copy.urlencode()

    context = {
        'polls': polls,
        'params': params,
        'search_term': search_term,
    }
    return render(request, 'polls/polls_list.html', context)


@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)

    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'polls/polls_list.html', context)


@login_required()
def polls_add(request):
    if request.user.has_perm('polls.add_poll'):
        if request.method == 'POST':
            form = PollAddForm(request.POST)
            # MODIFIED: Added () to call the is_valid method. CRITICAL FIX.
            if form.is_valid():
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                Choice(
                    poll=poll, choice_text=form.cleaned_data['choice1']).save()
                Choice(
                    poll=poll, choice_text=form.cleaned_data['choice2']).save()

                messages.success(
                    request, "Poll & Choices added successfully.", extra_tags='alert alert-success alert-dismissible fade show')

                return redirect('polls:list')
        else:
            form = PollAddForm()
        context = {
            'form': form,
        }
        return render(request, 'polls/add_poll.html', context)
    else:
        return HttpResponse("Sorry but you don't have permission to do that!")


@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        # MODIFIED: Added () to call the is_valid method. CRITICAL FIX.
        if form.is_valid():
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("polls:list")
    else:
        form = EditPollForm(instance=poll)

    return render(request, "polls/poll_edit.html", {'form': form, 'poll': poll})


@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')
    
    # MODIFIED: Actions that delete data should only be done via POST.
    if request.method == 'POST':
        poll.delete()
        messages.success(request, "Poll Deleted successfully.",
                       extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("polls:list")


@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST)
        # MODIFIED: Added () to call the is_valid method. CRITICAL FIX.
        if form.is_valid():
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm()
    return render(request, 'polls/add_choice.html', {'form': form})


@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    # MODIFIED: Avoided a redundant database query by accessing the poll directly.
    poll = choice.poll
    if request.user != poll.owner:
        return redirect('home')

    if request.method == 'POST':
        form = ChoiceAddForm(request.POST, instance=choice)
        # MODIFIED: Added () to call the is_valid method. CRITICAL FIX.
        if form.is_valid():
            form.save() # No need to set poll again, as it's an instance update
            messages.success(
                request, "Choice Updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('polls:edit', poll.id)
    else:
        form = ChoiceAddForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'polls/add_choice.html', context)


@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = choice.poll
    if request.user != poll.owner:
        return redirect('home')

    # MODIFIED: Actions that delete data should only be done via POST.
    if request.method == 'POST':
        choice.delete()
        messages.success(
            request, "Choice Deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('polls:edit', poll.id)


def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)

    if not poll.active:
        return render(request, 'polls/poll_result.html', {'poll': poll})
    
    # MODIFIED: Removed unnecessary loop_count and range logic.
    # The template can now loop through `poll.choice_set.all` directly.
    context = {
        'poll': poll,
    }
    return render(request, 'polls/poll_detail.html', context)


@login_required
def poll_vote(request, poll_id):
    # MODIFIED: Voting is a state-changing action, should only be POST.
    if request.method != 'POST':
        return HttpResponseBadRequest("Invalid request method.")

    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')

    if not poll.user_can_vote(request.user):
        messages.error(
            request, "You already voted on this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        return render(request, 'polls/poll_result.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("polls:detail", poll_id)
    # MODIFIED: Removed unreachable code that was here.


@login_required
def end_poll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('home')

    # MODIFIED: Ending a poll is a state-changing action, should only be POST.
    if request.method == 'POST':
        if poll.active:
            poll.active = False
            poll.save()
    
    # MODIFIED: Simplified logic. Always show the result after the action.
    return render(request, 'polls/poll_result.html', {'poll': poll})