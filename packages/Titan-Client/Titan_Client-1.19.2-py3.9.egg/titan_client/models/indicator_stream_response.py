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


class IndicatorStreamResponse(object):
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
        'cursor_next': 'str',
        'indicator_partial_result': 'bool',
        'indicator_total_count': 'int',
        'indicators': 'list[IndicatorSearchSchema]'
    }

    attribute_map = {
        'cursor_next': 'cursorNext',
        'indicator_partial_result': 'indicatorPartialResult',
        'indicator_total_count': 'indicatorTotalCount',
        'indicators': 'indicators'
    }

    def __init__(self, cursor_next=None, indicator_partial_result=None, indicator_total_count=None, indicators=None, local_vars_configuration=None):  # noqa: E501
        """IndicatorStreamResponse - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration.get_default_copy()
        self.local_vars_configuration = local_vars_configuration

        self._cursor_next = None
        self._indicator_partial_result = None
        self._indicator_total_count = None
        self._indicators = None
        self.discriminator = None

        if cursor_next is not None:
            self.cursor_next = cursor_next
        if indicator_partial_result is not None:
            self.indicator_partial_result = indicator_partial_result
        self.indicator_total_count = indicator_total_count
        if indicators is not None:
            self.indicators = indicators

    @property
    def cursor_next(self):
        """Gets the cursor_next of this IndicatorStreamResponse.  # noqa: E501

        Stream position identifier to continue scrolling from.  # noqa: E501

        :return: The cursor_next of this IndicatorStreamResponse.  # noqa: E501
        :rtype: str
        """
        return self._cursor_next

    @cursor_next.setter
    def cursor_next(self, cursor_next):
        """Sets the cursor_next of this IndicatorStreamResponse.

        Stream position identifier to continue scrolling from.  # noqa: E501

        :param cursor_next: The cursor_next of this IndicatorStreamResponse.  # noqa: E501
        :type cursor_next: str
        """

        self._cursor_next = cursor_next

    @property
    def indicator_partial_result(self):
        """Gets the indicator_partial_result of this IndicatorStreamResponse.  # noqa: E501

        Indicates whether response contains partial result. It could be in case when request took too long and was terminated by timeout.  # noqa: E501

        :return: The indicator_partial_result of this IndicatorStreamResponse.  # noqa: E501
        :rtype: bool
        """
        return self._indicator_partial_result

    @indicator_partial_result.setter
    def indicator_partial_result(self, indicator_partial_result):
        """Sets the indicator_partial_result of this IndicatorStreamResponse.

        Indicates whether response contains partial result. It could be in case when request took too long and was terminated by timeout.  # noqa: E501

        :param indicator_partial_result: The indicator_partial_result of this IndicatorStreamResponse.  # noqa: E501
        :type indicator_partial_result: bool
        """

        self._indicator_partial_result = indicator_partial_result

    @property
    def indicator_total_count(self):
        """Gets the indicator_total_count of this IndicatorStreamResponse.  # noqa: E501

        Total count of matched indicators.  # noqa: E501

        :return: The indicator_total_count of this IndicatorStreamResponse.  # noqa: E501
        :rtype: int
        """
        return self._indicator_total_count

    @indicator_total_count.setter
    def indicator_total_count(self, indicator_total_count):
        """Sets the indicator_total_count of this IndicatorStreamResponse.

        Total count of matched indicators.  # noqa: E501

        :param indicator_total_count: The indicator_total_count of this IndicatorStreamResponse.  # noqa: E501
        :type indicator_total_count: int
        """
        if self.local_vars_configuration.client_side_validation and indicator_total_count is None:  # noqa: E501
            raise ValueError("Invalid value for `indicator_total_count`, must not be `None`")  # noqa: E501

        self._indicator_total_count = indicator_total_count

    @property
    def indicators(self):
        """Gets the indicators of this IndicatorStreamResponse.  # noqa: E501

        List of `Indicators`.  # noqa: E501

        :return: The indicators of this IndicatorStreamResponse.  # noqa: E501
        :rtype: list[IndicatorSearchSchema]
        """
        return self._indicators

    @indicators.setter
    def indicators(self, indicators):
        """Sets the indicators of this IndicatorStreamResponse.

        List of `Indicators`.  # noqa: E501

        :param indicators: The indicators of this IndicatorStreamResponse.  # noqa: E501
        :type indicators: list[IndicatorSearchSchema]
        """

        self._indicators = indicators

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
        if not isinstance(other, IndicatorStreamResponse):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, IndicatorStreamResponse):
            return True

        return self.to_dict() != other.to_dict()
