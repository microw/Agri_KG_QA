from django.conf.urls import url
from . import index

from . import QA

urlpatterns = [
    url(r'^$', index.index_view),
    # url(r'^404', _404_view._404_),
    url(r'^qa', QA.question_answering),
]
