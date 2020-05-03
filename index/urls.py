from django.conf.urls import url
from . import views

app_name= 'index'

urlpatterns=[
    url(r'^$', views.first, name='first'),

    url(r'^user_register/$', views.usersign, name='user-sign'),

    url(r'^user_login/$', views.userlogin, name='user-login'),

    url(r'^user_logout/$', views.userlogout, name='user-logout'),

    url(r'^profile/$', views.profile_view, name='profile'),

    url(r'^profile_update/$', views.profile_update, name='profile-update'),

    url(r'^status/$', views.status_pat, name='pat-status'),

    url(r'^appointment/$', views.appointment_pat, name='pat-appoint'),

    url(r'^history/$', views.history_pat, name='pat-his'),



    url(r'^doc_register/$', views.docsign, name='doc-sign'),

    url(r'^doc_login/$', views.doclogin, name='doc-login'),

    url(r'^doc_logout/$', views.doclogout, name='doc-logout'),

    url(r'^doc_status/$', views.status_doc, name='doc-status'),

    url(r'^doc_profile/$', views.profile_view_doc, name='doc-profile'),

    url(r'^doc_profile_update/$', views.profile_update_doc, name='doc-profile-update'),

    url(r'^doc_appointment/$', views.appointment_doc, name='doc-appoint'),

    url(r'^doc_history/$', views.history_doc, name='doc-his'),
]
