# coding: utf-8

# flake8: noqa

"""
    Titan API v1

    # Introduction The Intel 471 API is organized around the principles of REST. Our API lets you gather results from our platform with anything that can send a HTTP request, including cURL and modern internet browsers. Access to this API requires an API token which is managed from your account settings.  Intel 471 reserves the right to add fields to our API however we will provide backwards compatibility and older version support so that it will be possible to choose exact versions that provide a response with an older structure. This documentation tracks all API versions and it is possible to compare this version which has changes highlighted. Please consider not storing information provided by API locally as we constantly improving our data set and want you to have the most updated information.  # Authentication Authenticate to the Intel 471 API by providing your API key in the request. Your API key carries many privileges so please do not expose them on public web resources.  Authentication to the API occurs by providing your email address as the login and API key as password in the authorization header via HTTP Basic Auth. Your API key can be found in the [API](https://portal.intel471.com/api) section on the portal.  # Accessing API ## Via internet browser Just open url: `https://api.intel471.com/v1/reports` Browser will ask for credentials, provide your email as login and API key as password. ## Via curl command line utility Type in terminal the following command: ``` curl -u <YOU EMAIL>:<YOUR API KEY> https://api.intel471.com/v1/reports ``` ## CURL usage examples This section covers some Watchers API requests.  ### List watcher groups: Type in terminal the following command:  *curl -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  ### Create watcher group: To create watcher group you need to pass a json body to request. Passing json body possible in two ways:  #### Write json to request *curl -d'{\"name\": \"group_name\", \"description\": \"Description\"}' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  #### Write json to file and call it *curl -d\"@json_file_name\" -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  ### Create free text search watcher: *curl -d'{\"type\": \"search\", \"freeTextPattern\": \"text to search\", \"notificationChannel\": \"website\"}' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups/\"GROUP UID\"/watchers*  ### Create specific search watcher: *curl -d'{\"type\": \"search\", \"patterns\":[ { \"types\": \"Actor\" , \"pattern\": \"swisman\" } ], \"notificationChannel\": \"website\" }' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups/\"GROUP UID\"/watchers*  ## Via Python Execute the following script: ``` import urllib2, base64  username = \"<YOU EMAIL>\" apikey = \"<YOUR API KEY>\"  request = urllib2.Request(\"https://api.intel471.com/v1/reports\") base64string = base64.encodestring('%s:%s' % (username, apikey)).replace('\\n', '') request.add_header(\"Authorization\", \"Basic %s\" % base64string) result = urllib2.urlopen(request) response_in_json = result.read()  print response_in_json ``` # API integration best practice with your application When accessing our API from your application don't do AJAX calls directly from web browser to https://api.intel471.com/. We do not allow CORS requests from browser due to potential security issues. Instead we suggest you look to establish a kind of a server side proxy in your application which will pass requests to our API.  For example: you can send a request from browser javascript to your server side, for instance to url `/apiproxy/actors?actor=hacker` which will be internally passed to `https://api.intel471.com/v1/actors?actor=hacker` (with authentication headers added) and response will be sent back to the browser.  # Versioning support We are consistently improving our API and occasionally bring in changes to the API based on customer feedback. The current API version can be seen in the drop down boxes for each version. We are providing API backwards compatibility when possible. All requests are prefixed with the major version number, for example `/v1`: ``` https://api.intel471.com/v1/reports ```  Different major versions are not compatible and imply significant response structure changes. Minor versions differences might include extra fields in response or provide new request parameter support. To stick to the specific version, just add the following extra parameter to the request, for example: `?v=1.2.0`. If you specify a not existing version, it will be brought down to the nearest existing one. For example, parameter `?v=1.5.4` will call API of version 1.3.0 — the latest available; `?v=1.2.9` will awake version 1.2.0 and so on.  Omitting the version parameter from your request means you will always use the latest version of the API.  We highly recommend you always add the version parameter to be safe on API updates and code your integration in a way to accept possible future extra fields added to the response object. ``` https://api.intel471.com/v1/tags?prettyPrint - will return response for the latest API version (v.1.1.0) https://api.intel471.com/v1/tags?prettyPrint&v=1.1.0 - absolutely the same request with the version explicitly specified https://api.intel471.com/v1/reports?prettyPrint&v=1.0.0 - will return response compatible with the older version ```   # noqa: E501

    The version of the OpenAPI document: 1.19.2
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

__version__ = "1.19.2"

# import apis into sdk package
from titan_client.api.actors_api import ActorsApi
from titan_client.api.alerts_api import AlertsApi
from titan_client.api.credentials_api import CredentialsApi
from titan_client.api.entities_api import EntitiesApi
from titan_client.api.events_api import EventsApi
from titan_client.api.forums_api import ForumsApi
from titan_client.api.girs_api import GIRsApi
from titan_client.api.global_search_api import GlobalSearchApi
from titan_client.api.iocs_api import IOCsApi
from titan_client.api.indicators_api import IndicatorsApi
from titan_client.api.messaging_services_api import MessagingServicesApi
from titan_client.api.news_api import NewsApi
from titan_client.api.pcap_api import PCAPApi
from titan_client.api.reports_api import ReportsApi
from titan_client.api.tags_api import TagsApi
from titan_client.api.vulnerabilities_api import VulnerabilitiesApi
from titan_client.api.watchers_api import WatchersApi
from titan_client.api.yara_api import YARAApi

# import ApiClient
from titan_client.api_client import ApiClient
from titan_client.configuration import Configuration
from titan_client.exceptions import OpenApiException
from titan_client.exceptions import ApiTypeError
from titan_client.exceptions import ApiValueError
from titan_client.exceptions import ApiKeyError
from titan_client.exceptions import ApiAttributeError
from titan_client.exceptions import ApiException
# import models into sdk package
from titan_client.models.alert_list_schema import AlertListSchema
from titan_client.models.alert_list_schema_chunks import AlertListSchemaChunks
from titan_client.models.alert_list_schema_highlights import AlertListSchemaHighlights
from titan_client.models.alert_list_schema_report import AlertListSchemaReport
from titan_client.models.alert_list_schema_response import AlertListSchemaResponse
from titan_client.models.credential_accessed_url_schema import CredentialAccessedUrlSchema
from titan_client.models.credential_accessed_url_schema_activity import CredentialAccessedUrlSchemaActivity
from titan_client.models.credential_accessed_url_schema_classification import CredentialAccessedUrlSchemaClassification
from titan_client.models.credential_accessed_url_schema_data import CredentialAccessedUrlSchemaData
from titan_client.models.credential_accessed_url_schema_data_credential import CredentialAccessedUrlSchemaDataCredential
from titan_client.models.credential_accessed_url_stream_schema import CredentialAccessedUrlStreamSchema
from titan_client.models.credential_accessed_urls_response import CredentialAccessedUrlsResponse
from titan_client.models.credential_accessed_urls_stream_response import CredentialAccessedUrlsStreamResponse
from titan_client.models.credential_occurrence_schema import CredentialOccurrenceSchema
from titan_client.models.credential_occurrence_schema_activity import CredentialOccurrenceSchemaActivity
from titan_client.models.credential_occurrence_schema_classification import CredentialOccurrenceSchemaClassification
from titan_client.models.credential_occurrence_schema_data import CredentialOccurrenceSchemaData
from titan_client.models.credential_occurrence_schema_data_credential import CredentialOccurrenceSchemaDataCredential
from titan_client.models.credential_occurrence_schema_data_credential_set import CredentialOccurrenceSchemaDataCredentialSet
from titan_client.models.credential_occurrences_response import CredentialOccurrencesResponse
from titan_client.models.credential_occurrences_stream_response import CredentialOccurrencesStreamResponse
from titan_client.models.credential_schema import CredentialSchema
from titan_client.models.credential_schema_activity import CredentialSchemaActivity
from titan_client.models.credential_schema_classification import CredentialSchemaClassification
from titan_client.models.credential_schema_data import CredentialSchemaData
from titan_client.models.credential_schema_data_credential_sets import CredentialSchemaDataCredentialSets
from titan_client.models.credential_schema_data_password import CredentialSchemaDataPassword
from titan_client.models.credential_schema_data_password_complexity import CredentialSchemaDataPasswordComplexity
from titan_client.models.credential_schema_statistics import CredentialSchemaStatistics
from titan_client.models.credential_set_accessed_url_schema import CredentialSetAccessedUrlSchema
from titan_client.models.credential_set_accessed_url_schema_activity import CredentialSetAccessedUrlSchemaActivity
from titan_client.models.credential_set_accessed_url_schema_classification import CredentialSetAccessedUrlSchemaClassification
from titan_client.models.credential_set_accessed_url_schema_data import CredentialSetAccessedUrlSchemaData
from titan_client.models.credential_set_accessed_url_schema_data_credential_set import CredentialSetAccessedUrlSchemaDataCredentialSet
from titan_client.models.credential_set_accessed_url_stream_schema import CredentialSetAccessedUrlStreamSchema
from titan_client.models.credential_set_accessed_url_stream_schema_data import CredentialSetAccessedUrlStreamSchemaData
from titan_client.models.credential_set_schema import CredentialSetSchema
from titan_client.models.credential_set_schema_activity import CredentialSetSchemaActivity
from titan_client.models.credential_set_schema_classification import CredentialSetSchemaClassification
from titan_client.models.credential_set_schema_data import CredentialSetSchemaData
from titan_client.models.credential_set_schema_data_external_sources import CredentialSetSchemaDataExternalSources
from titan_client.models.credential_set_schema_data_internal_sources import CredentialSetSchemaDataInternalSources
from titan_client.models.credential_set_schema_data_victims import CredentialSetSchemaDataVictims
from titan_client.models.credential_set_schema_statistics import CredentialSetSchemaStatistics
from titan_client.models.credential_set_stream_schema import CredentialSetStreamSchema
from titan_client.models.credential_set_stream_schema_data import CredentialSetStreamSchemaData
from titan_client.models.credential_sets_accessed_urls_response import CredentialSetsAccessedUrlsResponse
from titan_client.models.credential_sets_accessed_urls_stream_response import CredentialSetsAccessedUrlsStreamResponse
from titan_client.models.credential_sets_response import CredentialSetsResponse
from titan_client.models.credential_sets_stream_response import CredentialSetsStreamResponse
from titan_client.models.credentials_response import CredentialsResponse
from titan_client.models.credentials_stream_response import CredentialsStreamResponse
from titan_client.models.entities_response import EntitiesResponse
from titan_client.models.entities_schema import EntitiesSchema
from titan_client.models.entities_schema_links import EntitiesSchemaLinks
from titan_client.models.entities_schema_links_actors import EntitiesSchemaLinksActors
from titan_client.models.entities_schema_links_reports import EntitiesSchemaLinksReports
from titan_client.models.event_schema import EventSchema
from titan_client.models.event_schema_activity import EventSchemaActivity
from titan_client.models.event_schema_data import EventSchemaData
from titan_client.models.event_schema_data_event_data import EventSchemaDataEventData
from titan_client.models.event_schema_data_event_data_controller import EventSchemaDataEventDataController
from titan_client.models.event_schema_data_event_data_controller_geo_ip import EventSchemaDataEventDataControllerGeoIp
from titan_client.models.event_schema_data_event_data_controller_geo_ip_isp import EventSchemaDataEventDataControllerGeoIpIsp
from titan_client.models.event_schema_data_event_data_controllers import EventSchemaDataEventDataControllers
from titan_client.models.event_schema_data_event_data_encryption import EventSchemaDataEventDataEncryption
from titan_client.models.event_schema_data_event_data_file import EventSchemaDataEventDataFile
from titan_client.models.event_schema_data_event_data_location import EventSchemaDataEventDataLocation
from titan_client.models.event_schema_data_event_data_recipient_domains import EventSchemaDataEventDataRecipientDomains
from titan_client.models.event_schema_data_event_data_triggers import EventSchemaDataEventDataTriggers
from titan_client.models.event_schema_data_threat import EventSchemaDataThreat
from titan_client.models.event_schema_data_threat_data import EventSchemaDataThreatData
from titan_client.models.event_schema_meta import EventSchemaMeta
from titan_client.models.event_stream_response import EventStreamResponse
from titan_client.models.events_response import EventsResponse
from titan_client.models.full_breach_alert_schema import FullBreachAlertSchema
from titan_client.models.full_breach_alert_schema_all_of import FullBreachAlertSchemaAllOf
from titan_client.models.full_cve_schema import FullCveSchema
from titan_client.models.full_news_schema import FullNewsSchema
from titan_client.models.full_report_schema import FullReportSchema
from titan_client.models.full_report_schema_all_of import FullReportSchemaAllOf
from titan_client.models.full_spot_report_schema import FullSpotReportSchema
from titan_client.models.full_watcher_group_schema import FullWatcherGroupSchema
from titan_client.models.full_watcher_group_schema_all_of import FullWatcherGroupSchemaAllOf
from titan_client.models.full_watcher_group_schema_all_of_links import FullWatcherGroupSchemaAllOfLinks
from titan_client.models.full_watcher_group_schema_all_of_links_forum import FullWatcherGroupSchemaAllOfLinksForum
from titan_client.models.full_watcher_group_schema_all_of_links_thread import FullWatcherGroupSchemaAllOfLinksThread
from titan_client.models.full_watcher_group_schema_all_of_patterns import FullWatcherGroupSchemaAllOfPatterns
from titan_client.models.full_watcher_group_schema_all_of_watchers import FullWatcherGroupSchemaAllOfWatchers
from titan_client.models.gir_schema import GirSchema
from titan_client.models.gir_schema_data import GirSchemaData
from titan_client.models.gir_schema_data_gir import GirSchemaDataGir
from titan_client.models.girs_response import GirsResponse
from titan_client.models.indicator_search_response import IndicatorSearchResponse
from titan_client.models.indicator_search_schema import IndicatorSearchSchema
from titan_client.models.indicator_search_schema_activity import IndicatorSearchSchemaActivity
from titan_client.models.indicator_search_schema_data import IndicatorSearchSchemaData
from titan_client.models.indicator_search_schema_data_context import IndicatorSearchSchemaDataContext
from titan_client.models.indicator_search_schema_data_indicator_data import IndicatorSearchSchemaDataIndicatorData
from titan_client.models.indicator_search_schema_data_indicator_data_file import IndicatorSearchSchemaDataIndicatorDataFile
from titan_client.models.indicator_search_schema_data_threat import IndicatorSearchSchemaDataThreat
from titan_client.models.indicator_search_schema_data_threat_data import IndicatorSearchSchemaDataThreatData
from titan_client.models.indicator_search_schema_meta import IndicatorSearchSchemaMeta
from titan_client.models.indicator_stream_response import IndicatorStreamResponse
from titan_client.models.inline_object import InlineObject
from titan_client.models.inline_object1 import InlineObject1
from titan_client.models.instant_message_schema import InstantMessageSchema
from titan_client.models.instant_message_schema_activity import InstantMessageSchemaActivity
from titan_client.models.instant_message_schema_data import InstantMessageSchemaData
from titan_client.models.instant_message_schema_data_actor import InstantMessageSchemaDataActor
from titan_client.models.instant_message_schema_data_channel import InstantMessageSchemaDataChannel
from titan_client.models.instant_message_schema_data_message import InstantMessageSchemaDataMessage
from titan_client.models.instant_message_schema_data_message_attachments import InstantMessageSchemaDataMessageAttachments
from titan_client.models.instant_message_schema_data_server import InstantMessageSchemaDataServer
from titan_client.models.ioc_schema import IocSchema
from titan_client.models.ioc_schema_links import IocSchemaLinks
from titan_client.models.ioc_schema_links_actors import IocSchemaLinksActors
from titan_client.models.ioc_schema_links_reports import IocSchemaLinksReports
from titan_client.models.iocs_response import IocsResponse
from titan_client.models.malware import Malware
from titan_client.models.malware_reports_search_response import MalwareReportsSearchResponse
from titan_client.models.malware_reports_search_schema import MalwareReportsSearchSchema
from titan_client.models.malware_reports_search_schema_activity import MalwareReportsSearchSchemaActivity
from titan_client.models.malware_reports_search_schema_classification import MalwareReportsSearchSchemaClassification
from titan_client.models.malware_reports_search_schema_data import MalwareReportsSearchSchemaData
from titan_client.models.malware_reports_search_schema_data_malware_report_data import MalwareReportsSearchSchemaDataMalwareReportData
from titan_client.models.malware_reports_search_schema_data_malware_report_data_attachments import MalwareReportsSearchSchemaDataMalwareReportDataAttachments
from titan_client.models.malware_reports_search_schema_data_threat import MalwareReportsSearchSchemaDataThreat
from titan_client.models.malware_reports_search_schema_data_threat_data import MalwareReportsSearchSchemaDataThreatData
from titan_client.models.messaging_services_response import MessagingServicesResponse
from titan_client.models.news_schema import NewsSchema
from titan_client.models.news_schema_activity import NewsSchemaActivity
from titan_client.models.news_schema_data import NewsSchemaData
from titan_client.models.news_schema_data_attachments import NewsSchemaDataAttachments
from titan_client.models.pcap_response import PCAPResponse
from titan_client.models.pcap_schema import PCAPSchema
from titan_client.models.pcap_schema_data import PCAPSchemaData
from titan_client.models.pcap_schema_data_file import PCAPSchemaDataFile
from titan_client.models.pcap_schema_data_malware_family import PCAPSchemaDataMalwareFamily
from titan_client.models.pcap_schema_data_pcap import PCAPSchemaDataPcap
from titan_client.models.post_schema import PostSchema
from titan_client.models.post_schema_links import PostSchemaLinks
from titan_client.models.post_schema_links_author_actor import PostSchemaLinksAuthorActor
from titan_client.models.post_schema_links_forum import PostSchemaLinksForum
from titan_client.models.post_schema_links_thread import PostSchemaLinksThread
from titan_client.models.posts_response import PostsResponse
from titan_client.models.private_message_schema import PrivateMessageSchema
from titan_client.models.private_message_schema_links import PrivateMessageSchemaLinks
from titan_client.models.private_message_schema_links_author_actor import PrivateMessageSchemaLinksAuthorActor
from titan_client.models.private_message_schema_links_forum import PrivateMessageSchemaLinksForum
from titan_client.models.private_message_schema_links_recipient_actor import PrivateMessageSchemaLinksRecipientActor
from titan_client.models.private_messages_response import PrivateMessagesResponse
from titan_client.models.search_schema import SearchSchema
from titan_client.models.simple_actor_schema import SimpleActorSchema
from titan_client.models.simple_actor_schema_links import SimpleActorSchemaLinks
from titan_client.models.simple_actor_schema_links_contact_info import SimpleActorSchemaLinksContactInfo
from titan_client.models.simple_actor_schema_links_forums import SimpleActorSchemaLinksForums
from titan_client.models.simple_actor_schema_links_instant_message_servers import SimpleActorSchemaLinksInstantMessageServers
from titan_client.models.simple_actors_response import SimpleActorsResponse
from titan_client.models.simple_breach_alert_response import SimpleBreachAlertResponse
from titan_client.models.simple_breach_alert_schema import SimpleBreachAlertSchema
from titan_client.models.simple_breach_alert_schema_activity import SimpleBreachAlertSchemaActivity
from titan_client.models.simple_breach_alert_schema_data import SimpleBreachAlertSchemaData
from titan_client.models.simple_breach_alert_schema_data_breach_alert import SimpleBreachAlertSchemaDataBreachAlert
from titan_client.models.simple_breach_alert_schema_data_breach_alert_confidence import SimpleBreachAlertSchemaDataBreachAlertConfidence
from titan_client.models.simple_breach_alert_schema_data_breach_alert_sources import SimpleBreachAlertSchemaDataBreachAlertSources
from titan_client.models.simple_breach_alert_schema_data_breach_alert_victim import SimpleBreachAlertSchemaDataBreachAlertVictim
from titan_client.models.simple_breach_alert_schema_data_breach_alert_victim_industries import SimpleBreachAlertSchemaDataBreachAlertVictimIndustries
from titan_client.models.simple_breach_alert_schema_data_entities import SimpleBreachAlertSchemaDataEntities
from titan_client.models.simple_breach_alert_schema_data_geo_info import SimpleBreachAlertSchemaDataGeoInfo
from titan_client.models.simple_cve_schema import SimpleCveSchema
from titan_client.models.simple_cve_schema_activity import SimpleCveSchemaActivity
from titan_client.models.simple_cve_schema_classification import SimpleCveSchemaClassification
from titan_client.models.simple_cve_schema_data import SimpleCveSchemaData
from titan_client.models.simple_cve_schema_data_cve_report import SimpleCveSchemaDataCveReport
from titan_client.models.simple_cve_schema_data_cve_report_activity_location import SimpleCveSchemaDataCveReportActivityLocation
from titan_client.models.simple_cve_schema_data_cve_report_counter_measure_links import SimpleCveSchemaDataCveReportCounterMeasureLinks
from titan_client.models.simple_cve_schema_data_cve_report_cvss_score import SimpleCveSchemaDataCveReportCvssScore
from titan_client.models.simple_cve_schema_data_cve_report_exploit_status import SimpleCveSchemaDataCveReportExploitStatus
from titan_client.models.simple_cve_schema_data_cve_report_interest_level import SimpleCveSchemaDataCveReportInterestLevel
from titan_client.models.simple_cve_schema_data_cve_report_patch_links import SimpleCveSchemaDataCveReportPatchLinks
from titan_client.models.simple_cve_schema_data_cve_report_poc_links import SimpleCveSchemaDataCveReportPocLinks
from titan_client.models.simple_cve_schema_data_cve_report_titan_links import SimpleCveSchemaDataCveReportTitanLinks
from titan_client.models.simple_cves_response import SimpleCvesResponse
from titan_client.models.simple_news_response import SimpleNewsResponse
from titan_client.models.simple_report_schema import SimpleReportSchema
from titan_client.models.simple_report_schema_actor_subject_of_report import SimpleReportSchemaActorSubjectOfReport
from titan_client.models.simple_report_schema_classification import SimpleReportSchemaClassification
from titan_client.models.simple_report_schema_entities import SimpleReportSchemaEntities
from titan_client.models.simple_report_schema_locations import SimpleReportSchemaLocations
from titan_client.models.simple_report_schema_related_reports import SimpleReportSchemaRelatedReports
from titan_client.models.simple_report_schema_report_attachments import SimpleReportSchemaReportAttachments
from titan_client.models.simple_report_schema_sources import SimpleReportSchemaSources
from titan_client.models.simple_report_schema_victims import SimpleReportSchemaVictims
from titan_client.models.simple_reports_response import SimpleReportsResponse
from titan_client.models.simple_spot_report_schema import SimpleSpotReportSchema
from titan_client.models.simple_spot_report_schema_activity import SimpleSpotReportSchemaActivity
from titan_client.models.simple_spot_report_schema_data import SimpleSpotReportSchemaData
from titan_client.models.simple_spot_report_schema_data_entities import SimpleSpotReportSchemaDataEntities
from titan_client.models.simple_spot_report_schema_data_spot_report import SimpleSpotReportSchemaDataSpotReport
from titan_client.models.simple_spot_report_schema_data_spot_report_spot_report_data import SimpleSpotReportSchemaDataSpotReportSpotReportData
from titan_client.models.simple_spot_report_schema_data_spot_report_spot_report_data_links import SimpleSpotReportSchemaDataSpotReportSpotReportDataLinks
from titan_client.models.simple_spot_report_schema_data_spot_report_spot_report_data_victims import SimpleSpotReportSchemaDataSpotReportSpotReportDataVictims
from titan_client.models.simple_spot_reports_response import SimpleSpotReportsResponse
from titan_client.models.simple_watcher_group_schema import SimpleWatcherGroupSchema
from titan_client.models.situation_report_response import SituationReportResponse
from titan_client.models.situation_report_schema import SituationReportSchema
from titan_client.models.situation_report_schema_activity import SituationReportSchemaActivity
from titan_client.models.situation_report_schema_classification import SituationReportSchemaClassification
from titan_client.models.situation_report_schema_data import SituationReportSchemaData
from titan_client.models.situation_report_schema_data_situation_report import SituationReportSchemaDataSituationReport
from titan_client.models.situation_report_schema_data_situation_report_entities import SituationReportSchemaDataSituationReportEntities
from titan_client.models.situation_report_schema_data_situation_report_link import SituationReportSchemaDataSituationReportLink
from titan_client.models.situation_report_schema_data_situation_report_link_malware_family import SituationReportSchemaDataSituationReportLinkMalwareFamily
from titan_client.models.situation_report_schema_data_situation_report_link_malware_report import SituationReportSchemaDataSituationReportLinkMalwareReport
from titan_client.models.situation_report_schema_data_situation_report_victims import SituationReportSchemaDataSituationReportVictims
from titan_client.models.tag_response import TagResponse
from titan_client.models.tag_schema import TagSchema
from titan_client.models.watcher_group_response import WatcherGroupResponse
from titan_client.models.watcher_request_body import WatcherRequestBody
from titan_client.models.watcher_request_body_filters import WatcherRequestBodyFilters
from titan_client.models.watcher_request_body_patterns import WatcherRequestBodyPatterns
from titan_client.models.watcher_request_body_post import WatcherRequestBodyPost
from titan_client.models.watcher_request_body_post_all_of import WatcherRequestBodyPostAllOf
from titan_client.models.watcher_request_body_put import WatcherRequestBodyPut
from titan_client.models.watcher_request_body_put_all_of import WatcherRequestBodyPutAllOf
from titan_client.models.watcher_schema import WatcherSchema
from titan_client.models.watcher_schema_filters import WatcherSchemaFilters
from titan_client.models.watcher_schema_forum import WatcherSchemaForum
from titan_client.models.watcher_schema_links import WatcherSchemaLinks
from titan_client.models.watcher_schema_patterns import WatcherSchemaPatterns
from titan_client.models.watcher_schema_response import WatcherSchemaResponse
from titan_client.models.watcher_schema_thread import WatcherSchemaThread
from titan_client.models.yara_search_response import YARASearchResponse
from titan_client.models.yara_search_schema import YARASearchSchema
from titan_client.models.yara_search_schema_activity import YARASearchSchemaActivity
from titan_client.models.yara_search_schema_data import YARASearchSchemaData
from titan_client.models.yara_search_schema_data_threat import YARASearchSchemaDataThreat
from titan_client.models.yara_search_schema_data_threat_data import YARASearchSchemaDataThreatData
from titan_client.models.yara_search_schema_data_yara_data import YARASearchSchemaDataYaraData
from titan_client.models.yara_search_schema_meta import YARASearchSchemaMeta

