# coding: utf-8

"""
    Titan API v1

    # Introduction The Intel 471 API is organized around the principles of REST. Our API lets you gather results from our platform with anything that can send a HTTP request, including cURL and modern internet browsers. Access to this API requires an API token which is managed from your account settings.  Intel 471 reserves the right to add fields to our API however we will provide backwards compatibility and older version support so that it will be possible to choose exact versions that provide a response with an older structure. This documentation tracks all API versions and it is possible to compare this version which has changes highlighted. Please consider not storing information provided by API locally as we constantly improving our data set and want you to have the most updated information.  # Authentication Authenticate to the Intel 471 API by providing your API key in the request. Your API key carries many privileges so please do not expose them on public web resources.  Authentication to the API occurs by providing your email address as the login and API key as password in the authorization header via HTTP Basic Auth. Your API key can be found in the [API](https://portal.intel471.com/api) section on the portal.  # Accessing API ## Via internet browser Just open url: `https://api.intel471.com/v1/reports` Browser will ask for credentials, provide your email as login and API key as password. ## Via curl command line utility Type in terminal the following command: ``` curl -u <YOU EMAIL>:<YOUR API KEY> https://api.intel471.com/v1/reports ``` ## CURL usage examples This section covers some Watchers API requests.  ### List watcher groups: Type in terminal the following command:  *curl -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  ### Create watcher group: To create watcher group you need to pass a json body to request. Passing json body possible in two ways:  #### Write json to request *curl -d'{\"name\": \"group_name\", \"description\": \"Description\"}' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  #### Write json to file and call it *curl -d\"@json_file_name\" -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  ### Create free text search watcher: *curl -d'{\"type\": \"search\", \"freeTextPattern\": \"text to search\", \"notificationChannel\": \"website\"}' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups/\"GROUP UID\"/watchers*  ### Create specific search watcher: *curl -d'{\"type\": \"search\", \"patterns\":[ { \"types\": \"Actor\" , \"pattern\": \"swisman\" } ], \"notificationChannel\": \"website\" }' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups/\"GROUP UID\"/watchers*  ## Via Python Execute the following script: ``` import urllib2, base64  username = \"<YOU EMAIL>\" apikey = \"<YOUR API KEY>\"  request = urllib2.Request(\"https://api.intel471.com/v1/reports\") base64string = base64.encodestring('%s:%s' % (username, apikey)).replace('\\n', '') request.add_header(\"Authorization\", \"Basic %s\" % base64string) result = urllib2.urlopen(request) response_in_json = result.read()  print response_in_json ``` # API integration best practice with your application When accessing our API from your application don't do AJAX calls directly from web browser to https://api.intel471.com/. We do not allow CORS requests from browser due to potential security issues. Instead we suggest you look to establish a kind of a server side proxy in your application which will pass requests to our API.  For example: you can send a request from browser javascript to your server side, for instance to url `/apiproxy/actors?actor=hacker` which will be internally passed to `https://api.intel471.com/v1/actors?actor=hacker` (with authentication headers added) and response will be sent back to the browser.  # Versioning support We are consistently improving our API and occasionally bring in changes to the API based on customer feedback. The current API version can be seen in the drop down boxes for each version. We are providing API backwards compatibility when possible. All requests are prefixed with the major version number, for example `/v1`: ``` https://api.intel471.com/v1/reports ```  Different major versions are not compatible and imply significant response structure changes. Minor versions differences might include extra fields in response or provide new request parameter support. To stick to the specific version, just add the following extra parameter to the request, for example: `?v=1.2.0`. If you specify a not existing version, it will be brought down to the nearest existing one. For example, parameter `?v=1.5.4` will call API of version 1.3.0 — the latest available; `?v=1.2.9` will awake version 1.2.0 and so on.  Omitting the version parameter from your request means you will always use the latest version of the API.  We highly recommend you always add the version parameter to be safe on API updates and code your integration in a way to accept possible future extra fields added to the response object. ``` https://api.intel471.com/v1/tags?prettyPrint - will return response for the latest API version (v.1.1.0) https://api.intel471.com/v1/tags?prettyPrint&v=1.1.0 - absolutely the same request with the version explicitly specified https://api.intel471.com/v1/reports?prettyPrint&v=1.0.0 - will return response compatible with the older version ```   # noqa: E501

    The version of the OpenAPI document: 1.19.2
    Generated by: https://openapi-generator.tech
"""


try:
    from inspect import getfullargspec
except ImportError:
    from inspect import getargspec as getfullargspec
import pprint
import re  # noqa: F401
import six

from titan_client.configuration import Configuration
from titan_client.titan_stix.mappers.common import StixMapper


class WatcherSchema(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {
        'data_sets': 'list[str]',
        'description': 'str',
        'filter_by_gir_set': 'str',
        'filters': 'list[WatcherSchemaFilters]',
        'girs': 'list[str]',
        'links': 'list[WatcherSchemaLinks]',
        'muted': 'bool',
        'notification_channel': 'str',
        'notification_frequency': 'str',
        'patterns': 'list[WatcherSchemaPatterns]',
        'type': 'str',
        'uid': 'str'
    }

    attribute_map = {
        'data_sets': 'dataSets',
        'description': 'description',
        'filter_by_gir_set': 'filterByGirSet',
        'filters': 'filters',
        'girs': 'girs',
        'links': 'links',
        'muted': 'muted',
        'notification_channel': 'notificationChannel',
        'notification_frequency': 'notificationFrequency',
        'patterns': 'patterns',
        'type': 'type',
        'uid': 'uid'
    }

    def __init__(self, data_sets=None, description=None, filter_by_gir_set=None, filters=None, girs=None, links=None, muted=None, notification_channel=None, notification_frequency=None, patterns=None, type=None, uid=None, local_vars_configuration=None):  # noqa: E501
        """WatcherSchema - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._data_sets = None
        self._description = None
        self._filter_by_gir_set = None
        self._filters = None
        self._girs = None
        self._links = None
        self._muted = None
        self._notification_channel = None
        self._notification_frequency = None
        self._patterns = None
        self._type = None
        self._uid = None
        self.discriminator = None

        if data_sets is not None:
            self.data_sets = data_sets
        if description is not None:
            self.description = description
        if filter_by_gir_set is not None:
            self.filter_by_gir_set = filter_by_gir_set
        if filters is not None:
            self.filters = filters
        if girs is not None:
            self.girs = girs
        if links is not None:
            self.links = links
        self.muted = muted
        self.notification_channel = notification_channel
        self.notification_frequency = notification_frequency
        if patterns is not None:
            self.patterns = patterns
        self.type = type
        self.uid = uid

    @property
    def data_sets(self):
        """Gets the data_sets of this WatcherSchema.  # noqa: E501

        Data sets the watcher is limited by.  # noqa: E501

        :return: The data_sets of this WatcherSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._data_sets

    @data_sets.setter
    def data_sets(self, data_sets):
        """Sets the data_sets of this WatcherSchema.

        Data sets the watcher is limited by.  # noqa: E501

        :param data_sets: The data_sets of this WatcherSchema.  # noqa: E501
        :type data_sets: list[str]
        """

        self._data_sets = data_sets

    @property
    def description(self):
        """Gets the description of this WatcherSchema.  # noqa: E501

        Watcher `description`.  # noqa: E501

        :return: The description of this WatcherSchema.  # noqa: E501
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """Sets the description of this WatcherSchema.

        Watcher `description`.  # noqa: E501

        :param description: The description of this WatcherSchema.  # noqa: E501
        :type description: str
        """

        self._description = description

    @property
    def filter_by_gir_set(self):
        """Gets the filter_by_gir_set of this WatcherSchema.  # noqa: E501

        GIR set filter.  # noqa: E501

        :return: The filter_by_gir_set of this WatcherSchema.  # noqa: E501
        :rtype: str
        """
        return self._filter_by_gir_set

    @filter_by_gir_set.setter
    def filter_by_gir_set(self, filter_by_gir_set):
        """Sets the filter_by_gir_set of this WatcherSchema.

        GIR set filter.  # noqa: E501

        :param filter_by_gir_set: The filter_by_gir_set of this WatcherSchema.  # noqa: E501
        :type filter_by_gir_set: str
        """
        allowed_values = ["my_girs", "company_pirs", "custom"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and filter_by_gir_set not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `filter_by_gir_set` ({0}), must be one of {1}"  # noqa: E501
                .format(filter_by_gir_set, allowed_values)
            )

        self._filter_by_gir_set = filter_by_gir_set

    @property
    def filters(self):
        """Gets the filters of this WatcherSchema.  # noqa: E501

        Search filter of `search` watcher.  # noqa: E501

        :return: The filters of this WatcherSchema.  # noqa: E501
        :rtype: list[WatcherSchemaFilters]
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """Sets the filters of this WatcherSchema.

        Search filter of `search` watcher.  # noqa: E501

        :param filters: The filters of this WatcherSchema.  # noqa: E501
        :type filters: list[WatcherSchemaFilters]
        """

        self._filters = filters

    @property
    def girs(self):
        """Gets the girs of this WatcherSchema.  # noqa: E501

        GIR set paths defined by `filterByGirSet` param.  # noqa: E501

        :return: The girs of this WatcherSchema.  # noqa: E501
        :rtype: list[str]
        """
        return self._girs

    @girs.setter
    def girs(self, girs):
        """Sets the girs of this WatcherSchema.

        GIR set paths defined by `filterByGirSet` param.  # noqa: E501

        :param girs: The girs of this WatcherSchema.  # noqa: E501
        :type girs: list[str]
        """

        self._girs = girs

    @property
    def links(self):
        """Gets the links of this WatcherSchema.  # noqa: E501

        Links to the Forum and Thread of the `thread` type watcher.  # noqa: E501

        :return: The links of this WatcherSchema.  # noqa: E501
        :rtype: list[WatcherSchemaLinks]
        """
        return self._links

    @links.setter
    def links(self, links):
        """Sets the links of this WatcherSchema.

        Links to the Forum and Thread of the `thread` type watcher.  # noqa: E501

        :param links: The links of this WatcherSchema.  # noqa: E501
        :type links: list[WatcherSchemaLinks]
        """

        self._links = links

    @property
    def muted(self):
        """Gets the muted of this WatcherSchema.  # noqa: E501

        Watcher's mute status (if a watcher is muted, no alerts are received during its mute period)  # noqa: E501

        :return: The muted of this WatcherSchema.  # noqa: E501
        :rtype: bool
        """
        return self._muted

    @muted.setter
    def muted(self, muted):
        """Sets the muted of this WatcherSchema.

        Watcher's mute status (if a watcher is muted, no alerts are received during its mute period)  # noqa: E501

        :param muted: The muted of this WatcherSchema.  # noqa: E501
        :type muted: bool
        """
        if self.local_vars_configuration.client_side_validation and muted is None:  # noqa: E501
            raise ValueError("Invalid value for `muted`, must not be `None`")  # noqa: E501

        self._muted = muted

    @property
    def notification_channel(self):
        """Gets the notification_channel of this WatcherSchema.  # noqa: E501

        Notification chanel.  # noqa: E501

        :return: The notification_channel of this WatcherSchema.  # noqa: E501
        :rtype: str
        """
        return self._notification_channel

    @notification_channel.setter
    def notification_channel(self, notification_channel):
        """Sets the notification_channel of this WatcherSchema.

        Notification chanel.  # noqa: E501

        :param notification_channel: The notification_channel of this WatcherSchema.  # noqa: E501
        :type notification_channel: str
        """
        if self.local_vars_configuration.client_side_validation and notification_channel is None:  # noqa: E501
            raise ValueError("Invalid value for `notification_channel`, must not be `None`")  # noqa: E501
        allowed_values = ["email", "website"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and notification_channel not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `notification_channel` ({0}), must be one of {1}"  # noqa: E501
                .format(notification_channel, allowed_values)
            )

        self._notification_channel = notification_channel

    @property
    def notification_frequency(self):
        """Gets the notification_frequency of this WatcherSchema.  # noqa: E501

        Notification frequency.  # noqa: E501

        :return: The notification_frequency of this WatcherSchema.  # noqa: E501
        :rtype: str
        """
        return self._notification_frequency

    @notification_frequency.setter
    def notification_frequency(self, notification_frequency):
        """Sets the notification_frequency of this WatcherSchema.

        Notification frequency.  # noqa: E501

        :param notification_frequency: The notification_frequency of this WatcherSchema.  # noqa: E501
        :type notification_frequency: str
        """
        if self.local_vars_configuration.client_side_validation and notification_frequency is None:  # noqa: E501
            raise ValueError("Invalid value for `notification_frequency`, must not be `None`")  # noqa: E501
        allowed_values = ["immediately", "daily"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and notification_frequency not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `notification_frequency` ({0}), must be one of {1}"  # noqa: E501
                .format(notification_frequency, allowed_values)
            )

        self._notification_frequency = notification_frequency

    @property
    def patterns(self):
        """Gets the patterns of this WatcherSchema.  # noqa: E501

        Search query patterns applicable to a watcher of the `search` type.  # noqa: E501

        :return: The patterns of this WatcherSchema.  # noqa: E501
        :rtype: list[WatcherSchemaPatterns]
        """
        return self._patterns

    @patterns.setter
    def patterns(self, patterns):
        """Sets the patterns of this WatcherSchema.

        Search query patterns applicable to a watcher of the `search` type.  # noqa: E501

        :param patterns: The patterns of this WatcherSchema.  # noqa: E501
        :type patterns: list[WatcherSchemaPatterns]
        """

        self._patterns = patterns

    @property
    def type(self):
        """Gets the type of this WatcherSchema.  # noqa: E501

        Watcher `type`.  # noqa: E501

        :return: The type of this WatcherSchema.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this WatcherSchema.

        Watcher `type`.  # noqa: E501

        :param type: The type of this WatcherSchema.  # noqa: E501
        :type type: str
        """
        if self.local_vars_configuration.client_side_validation and type is None:  # noqa: E501
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["search", "thread"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and type not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def uid(self):
        """Gets the uid of this WatcherSchema.  # noqa: E501

        Watcher identifier.  # noqa: E501

        :return: The uid of this WatcherSchema.  # noqa: E501
        :rtype: str
        """
        return self._uid

    @uid.setter
    def uid(self, uid):
        """Sets the uid of this WatcherSchema.

        Watcher identifier.  # noqa: E501

        :param uid: The uid of this WatcherSchema.  # noqa: E501
        :type uid: str
        """
        if self.local_vars_configuration.client_side_validation and uid is None:  # noqa: E501
            raise ValueError("Invalid value for `uid`, must not be `None`")  # noqa: E501

        self._uid = uid

    def to_dict(self, serialize=False):
        """Returns the model properties as a dict"""
        result = {}

        def convert(x):
            if hasattr(x, "to_dict"):
                args = getfullargspec(x.to_dict).args
                if len(args) == 1:
                    return x.to_dict()
                else:
                    return x.to_dict(serialize)
            else:
                return x

        for attr, _ in six.iteritems(self.openapi_types):
            value = getattr(self, attr)
            attr = self.attribute_map.get(attr, attr) if serialize else attr
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: convert(x),
                    value
                ))
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], convert(item[1])),
                    value.items()
                ))
            else:
                result[attr] = convert(value)

        return result

    def to_stix(self):
        return StixMapper.map(self.to_dict(serialize=True))

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, WatcherSchema):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, WatcherSchema):
            return True

        return self.to_dict() != other.to_dict()
