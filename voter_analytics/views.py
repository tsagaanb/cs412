# voter_analytics/views.py

from django.shortcuts import render

# Create your views here.
from django.db.models.query import QuerySet
from django.views.generic import ListView, DetailView
from . models import Voter
from typing import Any
from django.utils import timezone
import plotly 
import plotly.graph_objects as go 
from django.db.models import Count
from django.utils.safestring import mark_safe



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
        context['voter_scores'] = list(range(0, 6)) 
        return context


class VoterDetailView(DetailView):
    ''' shows a page for a single voter '''

    template_name = 'voter_analytics/voter_detail.html'
    model = Voter
    context_object_name = 'voter'

class VoterGraphView(ListView):
    ''' shows a page for the Voter Data visualized by graphs '''

    template_name = 'voter_analytics/graphs.html'
    model = Voter

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
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        context = super().get_context_data(**kwargs)
        current_year = timezone.now().year
        context['years'] = list(range(1900, current_year + 1))
        context['voter_scores'] = list(range(0, 6)) 

        # 1. Histogram of Voters by Year of Birth
        birth_year_counts = queryset.values('date_of_birth__year').annotate(count=Count('id')).order_by('date_of_birth__year')
        x_years = [entry['date_of_birth__year'] for entry in birth_year_counts]
        y_counts = [entry['count'] for entry in birth_year_counts]

        fig1 = go.Figure(data=[go.Bar(x=x_years, y=y_counts)])
        fig1.update_layout(title="Voter Distribution by Year of Birth", xaxis_title="Year of Birth", yaxis_title="Count")
        context['graph1'] = mark_safe(fig1.to_html(full_html=False))

        # 2. Pie Chart of Party Affiliation Distribution
        party_counts = queryset.values('party_affiliation').annotate(count=Count('id')).order_by('party_affiliation')
        labels = [entry['party_affiliation'] for entry in party_counts]
        values = [entry['count'] for entry in party_counts]

        fig2 = go.Figure(data=[go.Pie(labels=labels, values=values)])
        fig2.update_layout(
            title="Voter Distribution by Party Affiliation",
            width=1000,  # Set width for pie chart
            height=1000  # Set height for pie chart
            )
        context['graph2'] = mark_safe(fig2.to_html(full_html=False))

        # 3. Histogram of Voter Participation in Elections
        election_data = {
            'Election': ['2020 State', '2021 Town', '2021 Primary', '2022 General', '2023 Town'],
            'Count': [
                queryset.filter(v20state=True).count(),
                queryset.filter(v21town=True).count(),
                queryset.filter(v21primary=True).count(),
                queryset.filter(v22general=True).count(),
                queryset.filter(v23town=True).count(),
            ]
        }
        fig3 = go.Figure(data=[go.Bar(x=election_data['Election'], y=election_data['Count'])])
        fig3.update_layout(title="Vote Count by Election", xaxis_title="Election", yaxis_title="Number of Voters")
        context['graph3'] = mark_safe(fig3.to_html(full_html=False))

        return context