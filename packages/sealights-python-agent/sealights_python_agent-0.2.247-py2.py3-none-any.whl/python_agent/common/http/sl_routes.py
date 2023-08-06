import sys

from python_agent import __package_name__ as PACKAGE_NAME
if sys.version_info < (3, 0):
    from urllib import quote as quote
else:
    from urllib.parse import quote as quote


class SLRoutes(object):
    RECOMMENDED = "recommended"
    BUILD_SESSION = "buildsession"
    RECOMMENDATIONS = "test-recommendations"
    EXCLUSIONS = "test-exclusions"
    LAB_IDS = "lab-ids"

    @staticmethod
    def build_session_v2(build_session_id=""):
        build_session_id = quote(build_session_id or "", safe="")
        return "/v2/agents/%s/%s" % (SLRoutes.BUILD_SESSION, build_session_id)

    @staticmethod
    def build_mapping_v3():
        return "/v3/agents/buildmapping"

    @staticmethod
    def build_mapping_v2():
        return "/v2/agents/buildmapping"

    @staticmethod
    def build_mapping_v3():
        return "/v3/agents/buildmapping"

    @staticmethod
    def footprints_v2():
        return "/v2/testfootprints"

    @staticmethod
    def footprints_v5():
        return "/v5/agents/footprints"

    @staticmethod
    def events_v1():
        return "/v1/testevents"

    @staticmethod
    def events_v2():
        return "/v2/agents/events"

    @staticmethod
    def test_execution_v3():
        return "/v3/testExecution"

    @staticmethod
    def external_data_v3():
        return "/v3/externaldata"

    @staticmethod
    def logsubmission_v2():
        return "/v2/logsubmission"

    @staticmethod
    def recommended_v2():
        return "/v2/agents/%s/%s" % (PACKAGE_NAME, SLRoutes.RECOMMENDED)

    @staticmethod
    def test_exclusions_v3(build_session_id, test_stage):
        return "/v3/%s/%s/%s" % (SLRoutes.EXCLUSIONS, build_session_id, SLRoutes.get_value_or_null(test_stage))

    @staticmethod
    def configuration_v2(customer_id, app_name, branch_name, test_stage, agent_name, agent_version):
        customer_id = SLRoutes.get_value_or_null(customer_id)
        app_name = SLRoutes.get_value_or_null(app_name)
        branch_name = SLRoutes.get_value_or_null(branch_name)
        test_stage = SLRoutes.get_value_or_null(test_stage)
        agent_name = SLRoutes.get_value_or_null(agent_name)
        agent_version = SLRoutes.get_value_or_null(agent_version)
        return "/v2/config/%s/%s/%s/%s/%s/%s" % (customer_id, app_name, branch_name, test_stage, agent_name, agent_version)

    @staticmethod
    def lab_ids_active_build_session_v1(labid):
        return "/v1/%s/%s/build-sessions/active" % (SLRoutes.LAB_IDS, labid)

    @staticmethod
    def get_value_or_null(value):
        return quote(value or "null", safe="")
