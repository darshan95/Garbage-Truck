# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import datetime
f = '%Y-%m-%d %H:%M:%S'

@auth.requires_login()
def index():
    session.user_id=auth.user.id
    session.user_name=auth.user.first_name
    if auth.has_membership(role='ghmc_admin'):
        redirect(URL('ghmc_official'))

    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    return dict()

@auth.requires_login()
@auth.requires_membership('ghmc_admin')
def ghmc_official():
    return dict()

"""    
def groupadd(check_group):
	if not db(db.auth_group.role==check_group).count():
        db.auth_group.insert(role=check_group)
"""

def worker_report():
    return dict()

@auth.requires_login()
def report_absence():
    form=SQLFORM(db.report_absent)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def rate_presence():
    form=SQLFORM(db.report_present)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def request_urgent():
    form=SQLFORM(db.request_festive)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def request_reservior():
    form=SQLFORM(db.request_collection)
    if form.process().accepted:
        session.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
@auth.requires_membership('ghmc_admin')
def request_reservior_view():
    s=db((db.request_collection.id>0) & (db.request_collection.user_id==db.auth_user.id) & (db.gmc_ward.user_id==auth.user.id)&(db.request_collection.pin==db.gmc_ward.pin)).select()
    d={}
    for i in s:
        dat=i.request_collection.request_on.date()
        #dat = i.request_collection.request_on.split()[0]
        if dat in d:
            d[dat]=d[dat]+[i]
        else:
            d[dat]=[i]
    return dict(d=d)

@auth.requires_login()
@auth.requires_membership('ghmc_admin')
def edit_status():
    d={}
    cid=request.args[0]
    d['Received']=1
    d['Observed']=2
    d['Verified']=3
    d['Processing']=4
    d['Completed']=5
    l=['a']
    form=FORM('Edit Status', 
            INPUT(_name='status',requires=IS_IN_SET(d.values())),
            INPUT(_type='submit'))
    if form.process().accepted:
        db(db.request_collection.id==cid).update(status=form.vars.status)
        session.flash = 'form accepted'
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
    return dict(form=form)

@auth.requires_login()
def view_requests_col():
    s=db((db.request_collection.id>0)&(auth.user.id==db.request_collection.user_id)).select()
    return dict(s=s)


@auth.requires_login()
@auth.requires_membership('ghmc_admin')
def request_urgent_view():
    s=db((db.request_festive.id>0) & (db.auth_user.id==db.request_festive.user_id)).select(orderby=~db.request_festive.request_on)
    d={}
    for i in s:
        #dat = i.request_festive.request_on.split()[0]
        dat = i.request_festive.request_on.date()
        if dat in d:
            d[dat]=d[dat]+[[i.auth_user.first_name, i.auth_user.last_name, i.request_festive.comment1,i.request_festive.reason]]
        else:
            d[dat]=[[i.auth_user.first_name, i.auth_user.last_name, i.request_festive.comment1, i.request_festive.reason]]
    return dict(d=d)    
            
@auth.requires_login()
@auth.requires_membership('ghmc_admin')
def absence_view():
    s=db((db.report_absent.id>0) & (db.report_absent.user_id==db.auth_user.id) & (db.auth_user.id==db.consumer.user_id) & (db.gmc_ward.user_id==auth.user.id)&(db.consumer.pin==db.gmc_ward.pin)).select(db.auth_user.first_name, db.auth_user.last_name, db.report_absent.request_on, db.report_absent.comment1,db.consumer.pin, orderby=~db.report_absent.request_on)
    d={}
    for i in s:
        #dat=datetime.datetime.strptime(i.report_absent.request_on,f).date()
        dat = i.report_absent.request_on.split()[0]
        if dat in d:
            d[dat]=d[dat]+[[i.auth_user.first_name, i.auth_user.last_name, i.report_absent.comment1]]
        else:
            d[dat]=[[i.auth_user.first_name, i.auth_user.last_name, i.report_absent.comment1]]
    return dict(d=d)
def presence_view():
    s=db((db.report_present.id>0) & (db.report_present.user_id==db.auth_user.id) & (db.auth_user.id==db.consumer.user_id) & (db.gmc_ward.user_id==auth.user.id)&(db.consumer.pin==db.gmc_ward.pin)&(db.report_present.ghmc_no==db.gmc_det.id)).select(db.auth_user.first_name, db.auth_user.last_name, db.report_present.request_on, db.report_present.comment1,db.consumer.pin,db.report_present.rating, db.gmc_det.worker_id, db.gmc_det.area, db.gmc_det.name, orderby=~db.report_present.rating)
    return dict(s=s)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
