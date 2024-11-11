# voter_analytics/views.py

from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter
from typing import Any
from django.utils import timezone



class VoterListView(ListView):
    ''' View to display the list of voters in Newton, MA '''

    template_name = 'voter_analytics/voters.html'
    model = Voter
    context_object_name = 'voters'
    paginate_by = 100

    def get_queryset(self):
        queryset = Voter.objects.all()

        # Filter by party affiliation
        party_affiliation = self.request.GET.get('party_affiliation')
        if party_affiliation:
            queryset = queryset.filter(party_affiliation=party_affiliation)

        # Filter by date of birth range
        min_dob = self.request.GET.get('min_dob')
        max_dob = self.request.GET.get('max_dob')
        if min_dob:
            queryset = queryset.filter(date_of_birth__year__gte=min_dob)
        if max_dob:
            queryset = queryset.filter(date_of_birth__year__lte=max_dob)

        # Filter by voter score
        voter_score = self.request.GET.get('voter_score')
        if voter_score:
            queryset = queryset.filter(voter_score=voter_score)

        # Filter by specific elections
        if self.request.GET.get('v20state') == 'on':
            queryset = queryset.filter(v20state=True)
        if self.request.GET.get('v21town') == 'on':
            queryset = queryset.filter(v21town=True)
        if self.request.GET.get('v21primary') == 'on':
            queryset = queryset.filter(v21primary=True)
        if self.request.GET.get('v22general') == 'on':
            queryset = queryset.filter(v22general=True)
        if self.request.GET.get('v23town') == 'on':
            queryset = queryset.filter(v23town=True)

        return queryset

    def get_context_data(self, **kwargs):
        ''' adds context for the filtering '''
        context = super().get_context_data(**kwargs)
        current_year = timezone.now().year
        context['years'] = list(range(1900, current_year + 1))
        context['voter_scores'] = list(range(0, 6))  # Adding voter score range (0 to 5)
        return context


class VoterDetailView(DetailView):
    ''' shows a page for a single voter '''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'