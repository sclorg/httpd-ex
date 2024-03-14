import os

import pytest
from pathlib import Path

from container_ci_suite.openshift import OpenShiftAPI

test_dir = Path(os.path.abspath(os.path.dirname(__file__)))

VERSION=os.getenv("SINGLE_VERSION")
if not VERSION:
    VERSION="2.4-el8"

class TestHTTPDExTemplate:

    def setup_method(self):
        self.oc_api = OpenShiftAPI(pod_name_prefix="httpd-example")
        json_raw_file = self.oc_api.get_raw_url_for_json(
            container="httpd-container", dir="imagestreams", filename="httpd-rhel.json"
        )
        self.oc_api.import_is(path=json_raw_file, name="httpd")

    def teardown_method(self):
        self.oc_api.delete_project()

    def test_httpd_ex_template_inside_cluster(self):
        template_json = self.oc_api.get_raw_url_for_json(
            container="httpd-ex", dir="openshift/templates", filename="httpd.json"
        )
        assert self.oc_api.deploy_template(
            template=template_json, name_in_template="httpd-example", expected_output="Welcome to your static httpd",
            openshift_args=["SOURCE_REPOSITORY_REF=master", f"HTTPD_VERSION={VERSION}", "NAME=httpd-example"]
        )
        assert self.oc_api.template_deployed(name_in_template="httpd-example")
        assert self.oc_api.check_response_inside_cluster(
            name_in_template="httpd-example", expected_output="Welcome to your static httpd"
        )

    def test_httpd_ex_template_by_request(self):
        template_json = self.oc_api.get_raw_url_for_json(
            container="httpd-ex", dir="openshift/templates", filename="httpd.json"
        )
        assert self.oc_api.deploy_template(
            template=template_json, name_in_template="httpd-example", expected_output="Welcome to your static httpd",
            openshift_args=["SOURCE_REPOSITORY_REF=master", f"HTTPD_VERSION={VERSION}", "NAME=httpd-example"]
        )
        assert self.oc_api.template_deployed(name_in_template="httpd-example")
        assert self.oc_api.check_response_outside_cluster(
            name_in_template="httpd-example", expected_output="Welcome to your static httpd"
        )
