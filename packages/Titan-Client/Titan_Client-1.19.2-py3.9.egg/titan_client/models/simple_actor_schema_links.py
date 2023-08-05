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


class SimpleActorSchemaLinks(object):
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
        'forum_post_total_count': 'int',
        'forum_private_message_total_count': 'int',
        'forum_total_count': 'int',
        'forums': 'list[SimpleActorSchemaLinksForums]',
        'instant_message_channel_total_count': 'int',
        'instant_message_server_total_count': 'int',
        'instant_message_servers': 'list[SimpleActorSchemaLinksInstantMessageServers]',
        'instant_message_total_count': 'int',
        'report_total_count': 'int',
        'reports': 'list[SimpleReportSchema]'
    }

    attribute_map = {
        'forum_post_total_count': 'forumPostTotalCount',
        'forum_private_message_total_count': 'forumPrivateMessageTotalCount',
        'forum_total_count': 'forumTotalCount',
        'forums': 'forums',
        'instant_message_channel_total_count': 'instantMessageChannelTotalCount',
        'instant_message_server_total_count': 'instantMessageServerTotalCount',
        'instant_message_servers': 'instantMessageServers',
        'instant_message_total_count': 'instantMessageTotalCount',
        'report_total_count': 'reportTotalCount',
        'reports': 'reports'
    }

    def __init__(self, forum_post_total_count=None, forum_private_message_total_count=None, forum_total_count=None, forums=None, instant_message_channel_total_count=None, instant_message_server_total_count=None, instant_message_servers=None, instant_message_total_count=None, report_total_count=None, reports=None, local_vars_configuration=None):  # noqa: E501
        """SimpleActorSchemaLinks - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._forum_post_total_count = None
        self._forum_private_message_total_count = None
        self._forum_total_count = None
        self._forums = None
        self._instant_message_channel_total_count = None
        self._instant_message_server_total_count = None
        self._instant_message_servers = None
        self._instant_message_total_count = None
        self._report_total_count = None
        self._reports = None
        self.discriminator = None

        self.forum_post_total_count = forum_post_total_count
        self.forum_private_message_total_count = forum_private_message_total_count
        self.forum_total_count = forum_total_count
        if forums is not None:
            self.forums = forums
        self.instant_message_channel_total_count = instant_message_channel_total_count
        self.instant_message_server_total_count = instant_message_server_total_count
        if instant_message_servers is not None:
            self.instant_message_servers = instant_message_servers
        self.instant_message_total_count = instant_message_total_count
        self.report_total_count = report_total_count
        if reports is not None:
            self.reports = reports

    @property
    def forum_post_total_count(self):
        """Gets the forum_post_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of linked posts.  # noqa: E501

        :return: The forum_post_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._forum_post_total_count

    @forum_post_total_count.setter
    def forum_post_total_count(self, forum_post_total_count):
        """Sets the forum_post_total_count of this SimpleActorSchemaLinks.

        Total count of linked posts.  # noqa: E501

        :param forum_post_total_count: The forum_post_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type forum_post_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and forum_post_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `forum_post_total_count`, must not be `None`")  # noqa: E501

        self._forum_post_total_count = forum_post_total_count

    @property
    def forum_private_message_total_count(self):
        """Gets the forum_private_message_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of linked private messages.  # noqa: E501

        :return: The forum_private_message_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._forum_private_message_total_count

    @forum_private_message_total_count.setter
    def forum_private_message_total_count(self, forum_private_message_total_count):
        """Sets the forum_private_message_total_count of this SimpleActorSchemaLinks.

        Total count of linked private messages.  # noqa: E501

        :param forum_private_message_total_count: The forum_private_message_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type forum_private_message_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and forum_private_message_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `forum_private_message_total_count`, must not be `None`")  # noqa: E501

        self._forum_private_message_total_count = forum_private_message_total_count

    @property
    def forum_total_count(self):
        """Gets the forum_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of linked forums.  # noqa: E501

        :return: The forum_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._forum_total_count

    @forum_total_count.setter
    def forum_total_count(self, forum_total_count):
        """Sets the forum_total_count of this SimpleActorSchemaLinks.

        Total count of linked forums.  # noqa: E501

        :param forum_total_count: The forum_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type forum_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and forum_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `forum_total_count`, must not be `None`")  # noqa: E501

        self._forum_total_count = forum_total_count

    @property
    def forums(self):
        """Gets the forums of this SimpleActorSchemaLinks.  # noqa: E501

        Linked forums.  # noqa: E501

        :return: The forums of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: list[SimpleActorSchemaLinksForums]
        """
        return self._forums

    @forums.setter
    def forums(self, forums):
        """Sets the forums of this SimpleActorSchemaLinks.

        Linked forums.  # noqa: E501

        :param forums: The forums of this SimpleActorSchemaLinks.  # noqa: E501
        :type forums: list[SimpleActorSchemaLinksForums]
        """

        self._forums = forums

    @property
    def instant_message_channel_total_count(self):
        """Gets the instant_message_channel_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of instant messaging channels of particular server actor participated in.  # noqa: E501

        :return: The instant_message_channel_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._instant_message_channel_total_count

    @instant_message_channel_total_count.setter
    def instant_message_channel_total_count(self, instant_message_channel_total_count):
        """Sets the instant_message_channel_total_count of this SimpleActorSchemaLinks.

        Total count of instant messaging channels of particular server actor participated in.  # noqa: E501

        :param instant_message_channel_total_count: The instant_message_channel_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type instant_message_channel_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and instant_message_channel_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `instant_message_channel_total_count`, must not be `None`")  # noqa: E501

        self._instant_message_channel_total_count = instant_message_channel_total_count

    @property
    def instant_message_server_total_count(self):
        """Gets the instant_message_server_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of linked instant messaging servers.  # noqa: E501

        :return: The instant_message_server_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._instant_message_server_total_count

    @instant_message_server_total_count.setter
    def instant_message_server_total_count(self, instant_message_server_total_count):
        """Sets the instant_message_server_total_count of this SimpleActorSchemaLinks.

        Total count of linked instant messaging servers.  # noqa: E501

        :param instant_message_server_total_count: The instant_message_server_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type instant_message_server_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and instant_message_server_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `instant_message_server_total_count`, must not be `None`")  # noqa: E501

        self._instant_message_server_total_count = instant_message_server_total_count

    @property
    def instant_message_servers(self):
        """Gets the instant_message_servers of this SimpleActorSchemaLinks.  # noqa: E501

        Linked instant messaging servers.  # noqa: E501

        :return: The instant_message_servers of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: list[SimpleActorSchemaLinksInstantMessageServers]
        """
        return self._instant_message_servers

    @instant_message_servers.setter
    def instant_message_servers(self, instant_message_servers):
        """Sets the instant_message_servers of this SimpleActorSchemaLinks.

        Linked instant messaging servers.  # noqa: E501

        :param instant_message_servers: The instant_message_servers of this SimpleActorSchemaLinks.  # noqa: E501
        :type instant_message_servers: list[SimpleActorSchemaLinksInstantMessageServers]
        """

        self._instant_message_servers = instant_message_servers

    @property
    def instant_message_total_count(self):
        """Gets the instant_message_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of instant messages actor has written on particular server.  # noqa: E501

        :return: The instant_message_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._instant_message_total_count

    @instant_message_total_count.setter
    def instant_message_total_count(self, instant_message_total_count):
        """Sets the instant_message_total_count of this SimpleActorSchemaLinks.

        Total count of instant messages actor has written on particular server.  # noqa: E501

        :param instant_message_total_count: The instant_message_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type instant_message_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and instant_message_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `instant_message_total_count`, must not be `None`")  # noqa: E501

        self._instant_message_total_count = instant_message_total_count

    @property
    def report_total_count(self):
        """Gets the report_total_count of this SimpleActorSchemaLinks.  # noqa: E501

        Total count of linked reports.  # noqa: E501

        :return: The report_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: int
        """
        return self._report_total_count

    @report_total_count.setter
    def report_total_count(self, report_total_count):
        """Sets the report_total_count of this SimpleActorSchemaLinks.

        Total count of linked reports.  # noqa: E501

        :param report_total_count: The report_total_count of this SimpleActorSchemaLinks.  # noqa: E501
        :type report_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and report_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `report_total_count`, must not be `None`")  # noqa: E501

        self._report_total_count = report_total_count

    @property
    def reports(self):
        """Gets the reports of this SimpleActorSchemaLinks.  # noqa: E501

        Linked reports. Array of simplified version of one of the following: `Information Report`, `Fintel Report`, `Malware Report`, `Spot Report`, `Situation Report`, `Breach Alert`.  # noqa: E501

        :return: The reports of this SimpleActorSchemaLinks.  # noqa: E501
        :rtype: list[SimpleReportSchema]
        """
        return self._reports

    @reports.setter
    def reports(self, reports):
        """Sets the reports of this SimpleActorSchemaLinks.

        Linked reports. Array of simplified version of one of the following: `Information Report`, `Fintel Report`, `Malware Report`, `Spot Report`, `Situation Report`, `Breach Alert`.  # noqa: E501

        :param reports: The reports of this SimpleActorSchemaLinks.  # noqa: E501
        :type reports: list[SimpleReportSchema]
        """

        self._reports = reports

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
        if not isinstance(other, SimpleActorSchemaLinks):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, SimpleActorSchemaLinks):
            return True

        return self.to_dict() != other.to_dict()
