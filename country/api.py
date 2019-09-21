from .models import Country, State
from tastypie.authentication import BasicAuthentication, SessionAuthentication, ApiKeyAuthentication, MultiAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, ReadOnlyAuthorization, Authorization
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie import fields
from jakhar.api import urlencodeSerializer



class CountryResource(ModelResource):
    class Meta:
        queryset = Country.objects.all()
        allowed_methods = ['get']
        resource_name = 'country'
        #excludes = ['password']
        limit = 0
        always_return_data = True
        filtering = {
        	'country_id': ALL,
        	'country_title': ALL
        }

        # filtering = {
        #     'username': 'exact'
        # }
        authorization = Authorization()
        authentication = Authentication()
        serializer = urlencodeSerializer()


class StateResource(ModelResource):
	state_ctid = fields.ForeignKey(CountryResource, 'state_ctid', full=True)
	class Meta:
		queryset = State.objects.all()
		allowed_methods = ['get']
		resource_name = 'state'
		#excludes = ['password']
		limit = 0
		always_return_data = True
		filtering = {
			'state_ctid': ALL_WITH_RELATIONS,
			'state_title': ALL
		}
		
		authorization = Authorization()
		authentication = Authentication()
		serializer = urlencodeSerializer()