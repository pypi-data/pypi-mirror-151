from textrank.views.pages import (
    IndexView, GroupsView, KeywordsView, RankView, WeightFormView, SamplesView,
    TopicsView
)

index = IndexView.as_view()
groups = GroupsView.as_view()
keywords = KeywordsView.as_view()
rank = RankView.as_view()
weightform = WeightFormView.as_view()
samples = SamplesView.as_view()
topics = TopicsView.as_view()
