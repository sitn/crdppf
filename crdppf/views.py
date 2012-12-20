from pyramid.response import Response
from pyramid.view import view_config

from .models import DBSession
from .models import Commune


def crdppf(request):

    
    #~ try:
        #~ one = DBSession.query(MyModel).filter(MyModel.name=='one').first()
    #~ except DBAPIError:
        #~ return Response(conn_err_msg, content_type='text/plain', status_int=500)
    one =12
    return {'one':one, 'project':'crdppf'}
