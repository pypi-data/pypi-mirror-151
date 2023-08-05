# coding: utf-8

"""
    Titan API v1

    # Introduction The Intel 471 API is organized around the principles of REST. Our API lets you gather results from our platform with anything that can send a HTTP request, including cURL and modern internet browsers. Access to this API requires an API token which is managed from your account settings.  Intel 471 reserves the right to add fields to our API however we will provide backwards compatibility and older version support so that it will be possible to choose exact versions that provide a response with an older structure. This documentation tracks all API versions and it is possible to compare this version which has changes highlighted. Please consider not storing information provided by API locally as we constantly improving our data set and want you to have the most updated information.  # Authentication Authenticate to the Intel 471 API by providing your API key in the request. Your API key carries many privileges so please do not expose them on public web resources.  Authentication to the API occurs by providing your email address as the login and API key as password in the authorization header via HTTP Basic Auth. Your API key can be found in the [API](https://portal.intel471.com/api) section on the portal.  # Accessing API ## Via internet browser Just open url: `https://api.intel471.com/v1/reports` Browser will ask for credentials, provide your email as login and API key as password. ## Via curl command line utility Type in terminal the following command: ``` curl -u <YOU EMAIL>:<YOUR API KEY> https://api.intel471.com/v1/reports ``` ## CURL usage examples This section covers some Watchers API requests.  ### List watcher groups: Type in terminal the following command:  *curl -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  ### Create watcher group: To create watcher group you need to pass a json body to request. Passing json body possible in two ways:  #### Write json to request *curl -d'{\"name\": \"group_name\", \"description\": \"Description\"}' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  #### Write json to file and call it *curl -d\"@json_file_name\" -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups*  ### Create free text search watcher: *curl -d'{\"type\": \"search\", \"freeTextPattern\": \"text to search\", \"notificationChannel\": \"website\"}' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups/\"GROUP UID\"/watchers*  ### Create specific search watcher: *curl -d'{\"type\": \"search\", \"patterns\":[ { \"types\": \"Actor\" , \"pattern\": \"swisman\" } ], \"notificationChannel\": \"website\" }' -X POST -u \"YOUR EMAIL\":\"YOUR API KEY\" https://api.intel471.com/v1/watcherGroups/\"GROUP UID\"/watchers*  ## Via Python Execute the following script: ``` import urllib2, base64  username = \"<YOU EMAIL>\" apikey = \"<YOUR API KEY>\"  request = urllib2.Request(\"https://api.intel471.com/v1/reports\") base64string = base64.encodestring('%s:%s' % (username, apikey)).replace('\\n', '') request.add_header(\"Authorization\", \"Basic %s\" % base64string) result = urllib2.urlopen(request) response_in_json = result.read()  print response_in_json ``` # API integration best practice with your application When accessing our API from your application don't do AJAX calls directly from web browser to https://api.intel471.com/. We do not allow CORS requests from browser due to potential security issues. Instead we suggest you look to establish a kind of a server side proxy in your application which will pass requests to our API.  For example: you can send a request from browser javascript to your server side, for instance to url `/apiproxy/actors?actor=hacker` which will be internally passed to `https://api.intel471.com/v1/actors?actor=hacker` (with authentication headers added) and response will be sent back to the browser.  # Versioning support We are consistently improving our API and occasionally bring in changes to the API based on customer feedback. The current API version can be seen in the drop down boxes for each version. We are providing API backwards compatibility when possible. All requests are prefixed with the major version number, for example `/v1`: ``` https://api.intel471.com/v1/reports ```  Different major versions are not compatible and imply significant response structure changes. Minor versions differences might include extra fields in response or provide new request parameter support. To stick to the specific version, just add the following extra parameter to the request, for example: `?v=1.2.0`. If you specify a not existing version, it will be brought down to the nearest existing one. For example, parameter `?v=1.5.4` will call API of version 1.3.0 — the latest available; `?v=1.2.9` will awake version 1.2.0 and so on.  Omitting the version parameter from your request means you will always use the latest version of the API.  We highly recommend you always add the version parameter to be safe on API updates and code your integration in a way to accept possible future extra fields added to the response object. ``` https://api.intel471.com/v1/tags?prettyPrint - will return response for the latest API version (v.1.1.0) https://api.intel471.com/v1/tags?prettyPrint&v=1.1.0 - absolutely the same request with the version explicitly specified https://api.intel471.com/v1/reports?prettyPrint&v=1.0.0 - will return response compatible with the older version ```   # noqa: E501

    The version of the OpenAPI document: 1.18.0
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import titan_client
from titan_client.models.search_schema import SearchSchema  # noqa: E501
from titan_client.rest import ApiException

class TestSearchSchema(unittest.TestCase):
    """SearchSchema unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test SearchSchema
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = titan_client.models.search_schema.SearchSchema()  # noqa: E501
        if include_optional :
            return SearchSchema(
                actor_total_count = 56, 
                actors = [
                    titan_client.models.simple_actor_schema.SimpleActorSchema(
                        active_from = 56, 
                        active_until = 56, 
                        handles = [
                            ''
                            ], 
                        last_updated = 56, 
                        links = titan_client.models.simple_actor_schema_links.SimpleActorSchema_links(
                            forum_post_total_count = 56, 
                            forum_private_message_total_count = 56, 
                            forum_total_count = 56, 
                            forums = [
                                titan_client.models.simple_actor_schema_links_forums.SimpleActorSchema_links_forums(
                                    actor_handle = '', 
                                    contact_info = [
                                        titan_client.models.simple_actor_schema_links_contact_info.SimpleActorSchema_links_contactInfo(
                                            type = '', 
                                            value = '', )
                                        ], 
                                    name = '', 
                                    time_zone = '', 
                                    uid = '', )
                                ], 
                            instant_message_channel_total_count = 56, 
                            instant_message_server_total_count = 56, 
                            instant_message_servers = [
                                titan_client.models.simple_actor_schema_links_instant_message_servers.SimpleActorSchema_links_instantMessageServers(
                                    name = '', 
                                    service_type = '', 
                                    uid = '', )
                                ], 
                            instant_message_total_count = 56, 
                            report_total_count = 56, 
                            reports = [
                                titan_client.models.simple_report_schema.SimpleReportSchema(
                                    actor_handle = '', 
                                    actor_subject_of_report = [
                                        titan_client.models.simple_report_schema_actor_subject_of_report.SimpleReportSchema_actorSubjectOfReport(
                                            aliases = [
                                                ''
                                                ], 
                                            handle = '', )
                                        ], 
                                    admiralty_code = 'C3', 
                                    classification = titan_client.models.simple_report_schema_classification.SimpleReportSchema_classification(
                                        intel_requirements = [
                                            ''
                                            ], ), 
                                    created = 56, 
                                    date_of_information = 56, 
                                    document_family = '', 
                                    document_type = '', 
                                    entities = [
                                        titan_client.models.simple_report_schema_entities.SimpleReportSchema_entities(
                                            type = '', 
                                            value = '', )
                                        ], 
                                    executive_summary = '', 
                                    last_updated = 56, 
                                    locations = [
                                        titan_client.models.simple_report_schema_locations.SimpleReportSchema_locations(
                                            country = '', 
                                            link = '', 
                                            region = '', )
                                        ], 
                                    motivation = [
                                        ''
                                        ], 
                                    portal_report_url = '', 
                                    related_reports = [
                                        titan_client.models.simple_report_schema_related_reports.SimpleReportSchema_relatedReports(
                                            document_family = '', 
                                            uid = '', )
                                        ], 
                                    released = 56, 
                                    report_attachments = [
                                        titan_client.models.simple_report_schema_report_attachments.SimpleReportSchema_reportAttachments(
                                            description = '', 
                                            file_name = '', 
                                            file_size = 56, 
                                            malicious = True, 
                                            mime_type = '', 
                                            url = '', )
                                        ], 
                                    sensitive_source = True, 
                                    source_characterization = '', 
                                    sources = [
                                        titan_client.models.simple_report_schema_sources.SimpleReportSchema_sources(
                                            index = 56, 
                                            title = '', 
                                            type = '', 
                                            url = '', )
                                        ], 
                                    subject = '', 
                                    tags = [
                                        ''
                                        ], 
                                    uid = '', 
                                    victims = [
                                        titan_client.models.simple_report_schema_victims.SimpleReportSchema_victims(
                                            name = '', 
                                            urls = [
                                                ''
                                                ], )
                                        ], )
                                ], ), 
                        uid = '', )
                    ], 
                breach_alerts = [
                    titan_client.models.simple_breach_alert_schema.SimpleBreachAlertSchema(
                        activity = titan_client.models.simple_breach_alert_schema_activity.SimpleBreachAlertSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.simple_breach_alert_schema_data.SimpleBreachAlertSchema_data(
                            breach_alert = titan_client.models.simple_breach_alert_schema_data_breach_alert.SimpleBreachAlertSchema_data_breach_alert(
                                actor_or_group = '', 
                                confidence = titan_client.models.simple_breach_alert_schema_data_breach_alert_confidence.SimpleBreachAlertSchema_data_breach_alert_confidence(
                                    description = '', 
                                    level = 'low', ), 
                                date_of_information = 56, 
                                intel_requirements = [
                                    ''
                                    ], 
                                released_at = 56, 
                                sensitive_source = True, 
                                sources = [
                                    titan_client.models.simple_breach_alert_schema_data_breach_alert_sources.SimpleBreachAlertSchema_data_breach_alert_sources(
                                        date = 56, 
                                        source_type = '', 
                                        title = '', 
                                        type = 'internal', 
                                        url = '', )
                                    ], 
                                title = '', 
                                victim = titan_client.models.simple_breach_alert_schema_data_breach_alert_victim.SimpleBreachAlertSchema_data_breach_alert_victim(
                                    industry = '', 
                                    name = '', 
                                    region = '', 
                                    revenue = '', 
                                    sector = '', 
                                    urls = [
                                        ''
                                        ], ), ), 
                            entities = [
                                titan_client.models.simple_breach_alert_schema_data_entities.SimpleBreachAlertSchema_data_entities(
                                    description = '', 
                                    geo_info = titan_client.models.simple_breach_alert_schema_data_geo_info.SimpleBreachAlertSchema_data_geo_info(
                                        country = '', 
                                        provider = '', ), 
                                    type = '', 
                                    value = '', )
                                ], ), 
                        last_updated = 56, 
                        uid = '', )
                    ], 
                breach_alerts_total_count = 56, 
                credential_occurrences = [
                    titan_client.models.credential_occurrence_schema.CredentialOccurrenceSchema(
                        activity = titan_client.models.credential_occurrence_schema_activity.CredentialOccurrenceSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        classification = titan_client.models.credential_occurrence_schema_classification.CredentialOccurrenceSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        data = titan_client.models.credential_occurrence_schema_data.CredentialOccurrenceSchema_data(
                            accessed_url = '', 
                            credential = titan_client.models.credential_occurrence_schema_data_credential.CredentialOccurrenceSchema_data_credential(
                                affiliations = [
                                    ''
                                    ], 
                                credential_domain = '', 
                                credential_login = '', 
                                detection_domain = '', 
                                password = titan_client.models.credential_schema_data_password.CredentialSchema_data_password(
                                    complexity = titan_client.models.credential_schema_data_password_complexity.CredentialSchema_data_password_complexity(
                                        entropy = 1.337, 
                                        length = 56, 
                                        lowercase = 56, 
                                        numbers = 56, 
                                        other = 56, 
                                        punctuation_marks = 56, 
                                        score = 1.337, 
                                        separators = 56, 
                                        symbols = 56, 
                                        uppercase = 56, 
                                        weakness = 1.337, ), 
                                    id = '', 
                                    password_plain = '', 
                                    strength = '', ), 
                                uid = '', ), 
                            credential_set = titan_client.models.credential_occurrence_schema_data_credential_set.CredentialOccurrenceSchema_data_credential_set(
                                name = '', 
                                uid = '', ), 
                            detected_malware = titan_client.models.malware.malware(
                                family = '', ), 
                            file_path = '', ), 
                        last_updated = 56, 
                        uid = '', )
                    ], 
                credential_occurrences_total_count = 56, 
                credential_sets = [
                    titan_client.models.credential_set_schema.CredentialSetSchema(
                        activity = titan_client.models.credential_set_schema_activity.CredentialSetSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        classification = titan_client.models.credential_set_schema_classification.CredentialSetSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        data = titan_client.models.credential_set_schema_data.CredentialSetSchema_data(
                            breach_date = 56, 
                            collection_date = 56, 
                            description = '', 
                            disclosure_date = 56, 
                            external_sources = [
                                titan_client.models.credential_set_schema_data_external_sources.CredentialSetSchema_data_external_sources(
                                    title = '', 
                                    url = '', )
                                ], 
                            internal_sources = [
                                titan_client.models.credential_set_schema_data_internal_sources.CredentialSetSchema_data_internal_sources(
                                    title = '', 
                                    url = '', )
                                ], 
                            name = '', 
                            record_count = 56, 
                            victims = [
                                titan_client.models.credential_set_schema_data_victims.CredentialSetSchema_data_victims(
                                    name = '', 
                                    urls = [
                                        ''
                                        ], )
                                ], ), 
                        last_updated = 56, 
                        statistics = titan_client.models.credential_set_schema_statistics.CredentialSetSchema_statistics(
                            accessed_urls_total_count = 56, 
                            credential_occurrences_total_count = 56, 
                            credentials_total_count = 56, ), 
                        uid = '', )
                    ], 
                credential_sets_total_count = 56, 
                credentials = [
                    titan_client.models.credential_schema.CredentialSchema(
                        activity = titan_client.models.credential_schema_activity.CredentialSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        classification = titan_client.models.credential_schema_classification.CredentialSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        data = titan_client.models.credential_schema_data.CredentialSchema_data(
                            affiliations = [
                                ''
                                ], 
                            credential_domain = '', 
                            credential_login = '', 
                            credential_sets = [
                                titan_client.models.credential_schema_data_credential_sets.CredentialSchema_data_credential_sets(
                                    name = '', 
                                    uid = '', )
                                ], 
                            detected_malware = [
                                titan_client.models.malware.malware(
                                    family = '', )
                                ], 
                            detection_domain = '', 
                            password = titan_client.models.credential_schema_data_password.CredentialSchema_data_password(
                                complexity = titan_client.models.credential_schema_data_password_complexity.CredentialSchema_data_password_complexity(
                                    entropy = 1.337, 
                                    length = 56, 
                                    lowercase = 56, 
                                    numbers = 56, 
                                    other = 56, 
                                    punctuation_marks = 56, 
                                    score = 1.337, 
                                    separators = 56, 
                                    symbols = 56, 
                                    uppercase = 56, 
                                    weakness = 1.337, ), 
                                id = '', 
                                password_plain = '', 
                                strength = '', ), ), 
                        last_updated = 56, 
                        statistics = titan_client.models.credential_schema_statistics.CredentialSchema_statistics(
                            accessed_urls_total_count = 56, ), 
                        uid = '', )
                    ], 
                credentials_total_count = 56, 
                cve_reports = [
                    titan_client.models.simple_cve_schema.SimpleCveSchema(
                        activity = titan_client.models.simple_cve_schema_activity.SimpleCveSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        classification = titan_client.models.simple_cve_schema_classification.SimpleCveSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        data = titan_client.models.simple_cve_schema_data.SimpleCveSchema_data(
                            cve_report = titan_client.models.simple_cve_schema_data_cve_report.SimpleCveSchema_data_cve_report(
                                activity_location = titan_client.models.simple_cve_schema_data_cve_report_activity_location.SimpleCveSchema_data_cve_report_activity_location(
                                    location_opensource = True, 
                                    location_private = True, 
                                    location_underground = True, ), 
                                counter_measure_links = [
                                    titan_client.models.simple_cve_schema_data_cve_report_counter_measure_links.SimpleCveSchema_data_cve_report_counter_measure_links(
                                        title = '', 
                                        url = '', )
                                    ], 
                                counter_measures = '', 
                                cpe = titan_client.models.cpe.cpe(), 
                                cve_status = '', 
                                cve_type = '', 
                                cvss_score = titan_client.models.simple_cve_schema_data_cve_report_cvss_score.SimpleCveSchema_data_cve_report_cvss_score(
                                    v2 = 1.337, 
                                    v3 = 1.337, ), 
                                detection = '', 
                                exploit_status = titan_client.models.simple_cve_schema_data_cve_report_exploit_status.SimpleCveSchema_data_cve_report_exploit_status(
                                    available = True, 
                                    not_observed = True, 
                                    productized = True, 
                                    weaponized = True, ), 
                                interest_level = titan_client.models.simple_cve_schema_data_cve_report_interest_level.SimpleCveSchema_data_cve_report_interest_level(
                                    disclosed_publicly = True, 
                                    exploit_sought = True, 
                                    researched_publicly = True, ), 
                                name = '', 
                                patch_links = [
                                    titan_client.models.simple_cve_schema_data_cve_report_patch_links.SimpleCveSchema_data_cve_report_patch_links(
                                        title = '', 
                                        url = '', )
                                    ], 
                                patch_status = '', 
                                poc = '', 
                                poc_links = [
                                    titan_client.models.simple_cve_schema_data_cve_report_poc_links.SimpleCveSchema_data_cve_report_poc_links(
                                        title = '', 
                                        url = '', )
                                    ], 
                                product_name = '', 
                                risk_level = '', 
                                summary = '', 
                                titan_links = [
                                    titan_client.models.simple_cve_schema_data_cve_report_titan_links.SimpleCveSchema_data_cve_report_titan_links(
                                        title = '', 
                                        url = '', )
                                    ], 
                                underground_activity = '', 
                                underground_activity_summary = '', 
                                vendor_name = '', ), ), 
                        last_updated = 56, 
                        uid = '', )
                    ], 
                cve_reports_total_count = 56, 
                entities = [
                    titan_client.models.entities_schema.EntitiesSchema(
                        last_updated = 56, 
                        links = titan_client.models.entities_schema_links.EntitiesSchema_links(
                            actor_total_count = 56, 
                            actors = [
                                titan_client.models.entities_schema_links_actors.EntitiesSchema_links_actors(
                                    handles = [
                                        ''
                                        ], 
                                    uid = '', )
                                ], 
                            report_total_count = 56, 
                            reports = [
                                titan_client.models.entities_schema_links_reports.EntitiesSchema_links_reports(
                                    admiralty_code = 'C3', 
                                    date_of_information = 56, 
                                    motivation = [
                                        ''
                                        ], 
                                    portal_report_url = '', 
                                    released = 56, 
                                    source_characterization = '', 
                                    subject = '', 
                                    uid = '', )
                                ], ), 
                        type = '', 
                        uid = '', 
                        value = '', )
                    ], 
                entity_total_count = 56, 
                event_total_count = 56, 
                events = [
                    titan_client.models.event_schema.EventSchema(
                        activity = titan_client.models.simple_cve_schema_activity.SimpleCveSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.event_schema_data.EventSchema_data(
                            event_data = titan_client.models.event_schema_data_event_data.EventSchema_data_event_data(
                                bot_settings = titan_client.models.bot_settings.bot_settings(), 
                                command = '', 
                                component_type = '', 
                                config_file = '', 
                                controller = titan_client.models.event_schema_data_event_data_controller.EventSchema_data_event_data_controller(
                                    geo_ip = titan_client.models.event_schema_data_event_data_controller_geo_ip.EventSchema_data_event_data_controller_geo_ip(
                                        city = '', 
                                        country = '', 
                                        country_code = '', 
                                        isp = titan_client.models.event_schema_data_event_data_controller_geo_ip_isp.EventSchema_data_event_data_controller_geo_ip_isp(
                                            autonomous_system = '', 
                                            network = '', 
                                            organization = '', ), 
                                        subdivision = [
                                            ''
                                            ], ), 
                                    ipv4 = '', 
                                    url = '', ), 
                                controllers = [
                                    titan_client.models.event_schema_data_event_data_controllers.EventSchema_data_event_data_controllers(
                                        url = '', )
                                    ], 
                                encryption = [
                                    titan_client.models.event_schema_data_event_data_encryption.EventSchema_data_event_data_encryption(
                                        algorithm = '', 
                                        context = '', 
                                        key = '', )
                                    ], 
                                exfil_location = '', 
                                file = titan_client.models.event_schema_data_event_data_file.EventSchema_data_event_data_file(
                                    download_url = '', 
                                    md5 = '', 
                                    sha1 = '', 
                                    sha256 = '', 
                                    size = 1.337, 
                                    type = '', ), 
                                inject_type = '', 
                                location = titan_client.models.event_schema_data_event_data_location.EventSchema_data_event_data_location(
                                    ipv4 = '', 
                                    url = '', ), 
                                plugin_name = '', 
                                plugin_type = '', 
                                recipient_domains = [
                                    titan_client.models.event_schema_data_event_data_recipient_domains.EventSchema_data_event_data_recipient_domains(
                                        count = 56, 
                                        domain = '', )
                                    ], 
                                senders = [
                                    ''
                                    ], 
                                settings = [
                                    None
                                    ], 
                                target_type = '', 
                                triggers = [
                                    titan_client.models.event_schema_data_event_data_triggers.EventSchema_data_event_data_triggers(
                                        trigger = '', )
                                    ], ), 
                            event_type = '', 
                            intel_requirements = [
                                ''
                                ], 
                            mitre_tactics = '', 
                            threat = titan_client.models.event_schema_data_threat.EventSchema_data_threat(
                                data = titan_client.models.event_schema_data_threat_data.EventSchema_data_threat_data(
                                    family = '', 
                                    malware_family_profile_uid = '', 
                                    variant = '', 
                                    version = '', ), 
                                type = '', 
                                uid = '', ), ), 
                        last_updated = 56, 
                        meta = titan_client.models.event_schema_meta.EventSchema_meta(
                            version = '', ), 
                        uid = '', )
                    ], 
                indicator_total_count = 56, 
                indicators = [
                    titan_client.models.indicator_search_schema.IndicatorSearchSchema(
                        activity = titan_client.models.indicator_search_schema_activity.IndicatorSearchSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.indicator_search_schema_data.IndicatorSearchSchema_data(
                            confidence = '', 
                            context = titan_client.models.indicator_search_schema_data_context.IndicatorSearchSchema_data_context(
                                description = '', ), 
                            expiration = 56, 
                            indicator_data = titan_client.models.indicator_search_schema_data_indicator_data.IndicatorSearchSchema_data_indicator_data(
                                address = '', 
                                file = titan_client.models.indicator_search_schema_data_indicator_data_file.IndicatorSearchSchema_data_indicator_data_file(
                                    download_url = '', 
                                    md5 = '', 
                                    sha1 = '', 
                                    sha256 = '', 
                                    size = 56, 
                                    type = '', ), 
                                geo_ip = titan_client.models.event_schema_data_event_data_controller_geo_ip.EventSchema_data_event_data_controller_geo_ip(
                                    city = '', 
                                    country = '', 
                                    country_code = '', 
                                    isp = titan_client.models.event_schema_data_event_data_controller_geo_ip_isp.EventSchema_data_event_data_controller_geo_ip_isp(
                                        autonomous_system = '', 
                                        network = '', 
                                        organization = '', ), 
                                    subdivision = [
                                        ''
                                        ], ), 
                                url = '', ), 
                            indicator_type = '', 
                            intel_requirements = [
                                ''
                                ], 
                            mitre_tactics = '', 
                            threat = titan_client.models.indicator_search_schema_data_threat.IndicatorSearchSchema_data_threat(
                                data = titan_client.models.indicator_search_schema_data_threat_data.IndicatorSearchSchema_data_threat_data(
                                    family = '', 
                                    malware_family_profile_uid = '', 
                                    variant = '', 
                                    version = '', ), 
                                type = '', 
                                uid = '', ), 
                            uid = '', ), 
                        last_updated = 56, 
                        meta = titan_client.models.indicator_search_schema_meta.IndicatorSearchSchema_meta(
                            version = '', ), 
                        uid = '', )
                    ], 
                instant_message_total_count = 56, 
                instant_messages = [
                    titan_client.models.instant_message_schema.InstantMessageSchema(
                        activity = titan_client.models.instant_message_schema_activity.InstantMessageSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.instant_message_schema_data.InstantMessageSchema_data(
                            actor = titan_client.models.instant_message_schema_data_actor.InstantMessageSchema_data_actor(
                                handle = '', 
                                uid = '', ), 
                            channel = titan_client.models.instant_message_schema_data_channel.InstantMessageSchema_data_channel(
                                name = '', 
                                registration_date = 56, 
                                topic = '', 
                                uid = '', 
                                url = '', ), 
                            message = titan_client.models.instant_message_schema_data_message.InstantMessageSchema_data_message(
                                attachments = [
                                    titan_client.models.instant_message_schema_data_message_attachments.InstantMessageSchema_data_message_attachments(
                                        height = 1.337, 
                                        original_url = '', 
                                        size = 1.337, 
                                        type = '', 
                                        uid = '', 
                                        width = 1.337, )
                                    ], 
                                reply_uid = '', 
                                text = '', 
                                uid = '', ), 
                            server = titan_client.models.instant_message_schema_data_server.InstantMessageSchema_data_server(
                                name = '', 
                                service_type = '', 
                                uid = '', ), ), 
                        last_updated = 56, )
                    ], 
                ioc_total_count = 56, 
                iocs = [
                    titan_client.models.ioc_schema.IocSchema(
                        active_from = 56, 
                        active_till = 56, 
                        isp_country_code = '', 
                        isp_name = '', 
                        last_updated = 56, 
                        links = titan_client.models.ioc_schema_links.IocSchema_links(
                            actor_total_count = 56, 
                            actors = [
                                titan_client.models.ioc_schema_links_actors.IocSchema_links_actors(
                                    handles = [
                                        ''
                                        ], 
                                    uid = '', )
                                ], 
                            report_total_count = 56, 
                            reports = [
                                titan_client.models.ioc_schema_links_reports.IocSchema_links_reports(
                                    admiralty_code = 'C3', 
                                    date_of_information = 56, 
                                    motivation = [
                                        ''
                                        ], 
                                    portal_report_url = '', 
                                    released = 56, 
                                    source_characterization = '', 
                                    subject = '', 
                                    uid = '', )
                                ], ), 
                        type = '', 
                        uid = '', 
                        value = '', )
                    ], 
                malware_report_total_count = 56, 
                malware_reports = [
                    titan_client.models.malware_reports_search_schema.MalwareReportsSearchSchema(
                        activity = titan_client.models.malware_reports_search_schema_activity.MalwareReportsSearchSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        classification = titan_client.models.malware_reports_search_schema_classification.MalwareReportsSearchSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        data = titan_client.models.malware_reports_search_schema_data.MalwareReportsSearchSchema_data(
                            malware_report_data = titan_client.models.malware_reports_search_schema_data_malware_report_data.MalwareReportsSearchSchema_data_malware_report_data(
                                attachments = [
                                    titan_client.models.malware_reports_search_schema_data_malware_report_data_attachments.MalwareReportsSearchSchema_data_malware_report_data_attachments(
                                        malicious = True, 
                                        mime_type = '', 
                                        name = '', 
                                        size = 56, 
                                        url = '', )
                                    ], 
                                related_reports = [
                                    ''
                                    ], 
                                released_at = 56, 
                                sensitive_source = True, 
                                text = '', 
                                title = '', ), 
                            threat = titan_client.models.malware_reports_search_schema_data_threat.MalwareReportsSearchSchema_data_threat(
                                data = titan_client.models.malware_reports_search_schema_data_threat_data.MalwareReportsSearchSchema_data_threat_data(
                                    family = '', 
                                    malware_family_profile_uid = '', 
                                    version = '', ), 
                                type = '', 
                                uid = '', ), ), 
                        last_updated = 56, 
                        meta = titan_client.models.indicator_search_schema_meta.IndicatorSearchSchema_meta(
                            version = '', ), 
                        uid = '', )
                    ], 
                news = [
                    titan_client.models.news_schema.NewsSchema(
                        activity = titan_client.models.news_schema_activity.NewsSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.news_schema_data.NewsSchema_data(
                            attachments = [
                                titan_client.models.news_schema_data_attachments.NewsSchema_data_attachments(
                                    malicious = True, 
                                    mime_type = '', 
                                    name = '', 
                                    size = 56, 
                                    url = '', )
                                ], 
                            released = 56, 
                            text = '', 
                            topic = '', 
                            type = 'BLOG', 
                            uid = '', ), 
                        last_updated = 56, )
                    ], 
                news_total_count = 56, 
                nids_list = titan_client.models.nids_search_schema.NIDSSearchSchema(
                    activity = titan_client.models.nids_search_schema_activity.NIDSSearchSchema_activity(
                        first = 56, 
                        last = 56, ), 
                    data = titan_client.models.nids_search_schema_data.NIDSSearchSchema_data(
                        confidence = '', 
                        intel_requirements = [
                            ''
                            ], 
                        nids_data = titan_client.models.nids_data.nids_data(), 
                        nids_type = '', 
                        threat = titan_client.models.nids_search_schema_data_threat.NIDSSearchSchema_data_threat(
                            data = titan_client.models.nids_search_schema_data_threat_data.NIDSSearchSchema_data_threat_data(
                                family = '', 
                                malware_family_profile_uid = '', 
                                version = '', ), 
                            type = '', 
                            uid = '', ), ), 
                    last_updated = 56, 
                    meta = titan_client.models.nids_search_schema_meta.NIDSSearchSchema_meta(
                        version = '', ), 
                    uid = '', ), 
                nids_total_count = 56, 
                post_total_count = 56, 
                posts = [
                    titan_client.models.post_schema.PostSchema(
                        date = 56, 
                        last_updated = 56, 
                        links = titan_client.models.post_schema_links.PostSchema_links(
                            author_actor = titan_client.models.post_schema_links_author_actor.PostSchema_links_authorActor(
                                handle = '', 
                                uid = '', ), 
                            forum = titan_client.models.post_schema_links_forum.PostSchema_links_forum(
                                description = '', 
                                name = '', 
                                uid = '', ), 
                            thread = titan_client.models.post_schema_links_thread.PostSchema_links_thread(
                                count = 56, 
                                topic = '', 
                                topic_original = '', 
                                uid = '', ), ), 
                        message = '', 
                        message_original = '', 
                        uid = '', )
                    ], 
                private_message_total_count = 56, 
                private_messages = [
                    titan_client.models.private_message_schema.PrivateMessageSchema(
                        date = 56, 
                        last_updated = 56, 
                        links = titan_client.models.private_message_schema_links.PrivateMessageSchema_links(
                            author_actor = titan_client.models.private_message_schema_links_author_actor.PrivateMessageSchema_links_authorActor(
                                handle = '', 
                                uid = '', ), 
                            forum = titan_client.models.private_message_schema_links_forum.PrivateMessageSchema_links_forum(
                                description = '', 
                                name = '', 
                                uid = '', ), 
                            recipient_actor = titan_client.models.private_message_schema_links_recipient_actor.PrivateMessageSchema_links_recipientActor(
                                handle = '', 
                                uid = '', ), ), 
                        message = '', 
                        message_original = '', 
                        subject = '', 
                        subject_original = '', 
                        uid = '', )
                    ], 
                report_total_count = 56, 
                reports = [
                    titan_client.models.simple_report_schema.SimpleReportSchema(
                        actor_handle = '', 
                        actor_subject_of_report = [
                            titan_client.models.simple_report_schema_actor_subject_of_report.SimpleReportSchema_actorSubjectOfReport(
                                aliases = [
                                    ''
                                    ], 
                                handle = '', )
                            ], 
                        admiralty_code = 'C3', 
                        classification = titan_client.models.simple_report_schema_classification.SimpleReportSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        created = 56, 
                        date_of_information = 56, 
                        document_family = '', 
                        document_type = '', 
                        entities = [
                            titan_client.models.simple_report_schema_entities.SimpleReportSchema_entities(
                                type = '', 
                                value = '', )
                            ], 
                        executive_summary = '', 
                        last_updated = 56, 
                        locations = [
                            titan_client.models.simple_report_schema_locations.SimpleReportSchema_locations(
                                country = '', 
                                link = '', 
                                region = '', )
                            ], 
                        motivation = [
                            ''
                            ], 
                        portal_report_url = '', 
                        related_reports = [
                            titan_client.models.simple_report_schema_related_reports.SimpleReportSchema_relatedReports(
                                document_family = '', 
                                uid = '', )
                            ], 
                        released = 56, 
                        report_attachments = [
                            titan_client.models.simple_report_schema_report_attachments.SimpleReportSchema_reportAttachments(
                                description = '', 
                                file_name = '', 
                                file_size = 56, 
                                malicious = True, 
                                mime_type = '', 
                                url = '', )
                            ], 
                        sensitive_source = True, 
                        source_characterization = '', 
                        sources = [
                            titan_client.models.simple_report_schema_sources.SimpleReportSchema_sources(
                                index = 56, 
                                title = '', 
                                type = '', 
                                url = '', )
                            ], 
                        subject = '', 
                        tags = [
                            ''
                            ], 
                        uid = '', 
                        victims = [
                            titan_client.models.simple_report_schema_victims.SimpleReportSchema_victims(
                                name = '', 
                                urls = [
                                    ''
                                    ], )
                            ], )
                    ], 
                situation_reports = [
                    titan_client.models.situation_report_schema.SituationReportSchema(
                        activity = titan_client.models.situation_report_schema_activity.SituationReportSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        classification = titan_client.models.situation_report_schema_classification.SituationReportSchema_classification(
                            intel_requirements = [
                                ''
                                ], ), 
                        data = titan_client.models.situation_report_schema_data.SituationReportSchema_data(
                            situation_report = titan_client.models.situation_report_schema_data_situation_report.SituationReportSchema_data_situation_report(
                                entities = [
                                    titan_client.models.situation_report_schema_data_situation_report_entities.SituationReportSchema_data_situation_report_entities(
                                        type = '', 
                                        value = '', )
                                    ], 
                                link = titan_client.models.situation_report_schema_data_situation_report_link.SituationReportSchema_data_situation_report_link(
                                    malware_family = titan_client.models.situation_report_schema_data_situation_report_link_malware_family.SituationReportSchema_data_situation_report_link_malware_family(
                                        uid = '', ), 
                                    malware_report = titan_client.models.situation_report_schema_data_situation_report_link_malware_report.SituationReportSchema_data_situation_report_link_malware_report(
                                        uid = '', ), ), 
                                related_reports = [
                                    ''
                                    ], 
                                released_at = 56, 
                                sensitive_source = True, 
                                text = '', 
                                title = '', 
                                victims = [
                                    titan_client.models.situation_report_schema_data_situation_report_victims.SituationReportSchema_data_situation_report_victims(
                                        name = '', 
                                        urls = [
                                            ''
                                            ], )
                                    ], ), ), 
                        last_updated = 56, 
                        uid = '', )
                    ], 
                situation_reports_total_count = 56, 
                spot_reports = [
                    titan_client.models.simple_spot_report_schema.SimpleSpotReportSchema(
                        activity = titan_client.models.simple_spot_report_schema_activity.SimpleSpotReportSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.simple_spot_report_schema_data.SimpleSpotReportSchema_data(
                            entities = [
                                titan_client.models.simple_report_schema_entities.SimpleReportSchema_entities(
                                    type = '', 
                                    value = '', )
                                ], 
                            spot_report = titan_client.models.simple_spot_report_schema_data_spot_report.SimpleSpotReportSchema_data_spot_report(
                                spot_report_data = titan_client.models.simple_spot_report_schema_data_spot_report_spot_report_data.SimpleSpotReportSchema_data_spot_report_spot_report_data(
                                    date_of_information = 56, 
                                    intel_requirements = [
                                        ''
                                        ], 
                                    links = [
                                        titan_client.models.simple_spot_report_schema_data_spot_report_spot_report_data_links.SimpleSpotReportSchema_data_spot_report_spot_report_data_links(
                                            title = '', 
                                            type = '', 
                                            url = '', )
                                        ], 
                                    related_reports = [
                                        ''
                                        ], 
                                    released_at = 56, 
                                    sensitive_source = True, 
                                    text = '', 
                                    title = '', 
                                    version = '', 
                                    victims = [
                                        titan_client.models.simple_spot_report_schema_data_spot_report_spot_report_data_victims.SimpleSpotReportSchema_data_spot_report_spot_report_data_victims(
                                            name = '', 
                                            urls = [
                                                ''
                                                ], )
                                        ], ), 
                                uid = '', ), ), 
                        last_updated = 56, 
                        uid = '', )
                    ], 
                spot_reports_total_count = 56, 
                yara_total_count = 56, 
                yaras = [
                    titan_client.models.yara_search_schema.YARASearchSchema(
                        activity = titan_client.models.yara_search_schema_activity.YARASearchSchema_activity(
                            first = 56, 
                            last = 56, ), 
                        data = titan_client.models.yara_search_schema_data.YARASearchSchema_data(
                            confidence = '', 
                            intel_requirements = [
                                ''
                                ], 
                            threat = titan_client.models.yara_search_schema_data_threat.YARASearchSchema_data_threat(
                                data = titan_client.models.yara_search_schema_data_threat_data.YARASearchSchema_data_threat_data(
                                    family = '', 
                                    malware_family_profile_uid = '', 
                                    version = '', ), 
                                type = '', 
                                uid = '', ), 
                            yara_data = titan_client.models.yara_search_schema_data_yara_data.YARASearchSchema_data_yara_data(
                                signature = '', 
                                title = '', ), ), 
                        last_updated = 56, 
                        meta = titan_client.models.yara_search_schema_meta.YARASearchSchema_meta(
                            version = '', ), 
                        uid = '', )
                    ]
            )
        else :
            return SearchSchema(
                actor_total_count = 56,
                breach_alerts_total_count = 56,
                credential_occurrences_total_count = 56,
                credential_sets_total_count = 56,
                credentials_total_count = 56,
                cve_reports_total_count = 56,
                entity_total_count = 56,
                event_total_count = 56,
                indicator_total_count = 56,
                instant_message_total_count = 56,
                ioc_total_count = 56,
                malware_report_total_count = 56,
                news_total_count = 56,
                nids_total_count = 56,
                post_total_count = 56,
                private_message_total_count = 56,
                report_total_count = 56,
                situation_reports_total_count = 56,
                spot_reports_total_count = 56,
                yara_total_count = 56,
        )

    def testSearchSchema(self):
        """Test SearchSchema"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
