from django.conf.urls import url
from . import views

app_name= 'index'

urlpatterns=[
    url(r'^$', views.first, name='first'),

    url(r'^user_register/$', views.usersign, name='user-sign'),

    url(r'^user_login/$', views.userlogin, name='user-login'),

    url(r'^user_logout/$', views.userlogout, name='user-logout'),

    url(r'^doc_register/$', views.doc_signup, name='doc_signup'),

    url(r'^doc_login/$', views.doc_signin, name='doc_signin'),

    url(r'^doc_logout/$', views.doclogout, name='doc-logout'),

    url(r'^profile/$', views.profile_view, name='profile'),

    url(r'^profile_update/$', views.profile_update, name='profile-update'),

    url(r'^status/$', views.status_pat, name='pat-status'),

    url(r'^appointment/$', views.appointment_pat, name='pat-appoint'),

    url(r'^history/$', views.history_pat, name='pat-his'),

     url(r'profile_doc/$', views.doc_profile, name='doc_profile'),

    url(r'profile/edit/$', views.edit_doc_profile, name='edit_profile'),

    url(r'profile/change_password/$', views.change_password, name='change_password'),
]
