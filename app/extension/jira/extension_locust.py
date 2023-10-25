import re
from locustio.common_utils import init_logger, jira_measure, run_as_specific_user, raise_if_login_failed  # noqa F401

logger = init_logger(app_type='jira')


# @jira_measure("locust_app_specific_action")
# # @run_as_specific_user(username='admin', password='admin')  # run as specific user
# def app_specific_action(locust):
#     r = locust.get('/app/get_endpoint', catch_response=True)  # call app-specific GET endpoint
#     content = r.content.decode('utf-8')   # decode response content
#
#     token_pattern_example = '"token":"(.+?)"'
#     id_pattern_example = '"id":"(.+?)"'
#     token = re.findall(token_pattern_example, content)  # get TOKEN from response using regexp
#     id = re.findall(id_pattern_example, content)    # get ID from response using regexp
#
#     logger.locust_info(f'token: {token}, id: {id}')  # log info for debug when verbose is true in jira.yml file
#     if 'assertion string' not in content:
#         logger.error(f"'assertion string' was not found in {content}")
#     assert 'assertion string' in content  # assert specific string in response content
#
#     body = {"id": id, "token": token}  # include parsed variables to POST request body
#     headers = {'content-type': 'application/json'}
#     r = locust.post('/app/post_endpoint', body, headers, catch_response=True)  # call app-specific POST endpoint
#     content = r.content.decode('utf-8')
#     if 'assertion string after successful POST request' not in content:
#         logger.error(f"'assertion string after successful POST request' was not found in {content}")
#     assert 'assertion string after successful POST request' in content  # assertion after POST request

@jira_measure("locust_app_specific_action_config")
@run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    raise_if_login_failed(locust)
    r = locust.get('/rest/datarocks/1.0/configuration', catch_response=True)
    response_json = r.json()
    assert 'hideJiraSearchField' in response_json, "invalid response from combined-search config endpoint"


@jira_measure("locust_app_specific_action_jira_search")
# @run_as_specific_user(username='admin', password='admin')  # run as specific user
def app_specific_action(locust):
    raise_if_login_failed(locust)
    data = {
        'searchTerm': "AppIssue",
        'pagination': {
            'limit': 20,
            'offset': 0
        }
    }
    r = locust.post('/rest/datarocks/1.0/search/jira', catch_response=True, json=data)
    response_json = r.json()
    assert 'searchValid' in response_json, "invalid response from combined-search search/jira endpoint"
    assert response_json['searchValid'] is True, "invalid response from combined-search search/jira endpoint"
    assert 'resultList' in response_json, "invalid response from combined-search search/jira endpoint"
    assert len(response_json['resultList']) > 0, "invalid response from combined-search search/jira endpoint"