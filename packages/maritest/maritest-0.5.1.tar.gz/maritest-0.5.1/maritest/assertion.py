import json
from typing import Any, Optional

from maritest.utils.dict_lookups import keys_in_dict

from .client import Http
from lxml import html


class Assert(Http):
    """
    Base class for collection assertion
    test. All of these listing method are implemented
    based on abstract method in Http class
    """

    def assert_is_ok(self, message: str):
        """Assert request is ok"""
        if self.response.status_code != 200:
            message = "The request didn't success"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_failed(self, message: str):
        """Assert request is failed"""
        if self.response.status_code == 200:
            message = "The request should be failed"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_headers(self, message: str):
        """Assert response has headers"""
        if not self.response.headers:
            message = "There's no headers in that request"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_content_type(self, message: str):
        """Assert response has content-type header"""
        # this one is much more specific
        # to body information
        if not self.response.headers["Content-Type"]:
            message = "Perhaps 'content-type' wasn't set"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_content_type_to_equal(self, value: str, message: str):
        """Assert content-type header equal to expected result"""
        # validate expected content-type
        # with actual result in response
        if value != self.response.headers["Content-Type"]:
            message = "The value of content-type doesn't match with the actual result"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_is_2xx_status(self, message: str):
        """Assert response in range 2xx status code"""
        if not 200 <= self.response.status_code < 300:
            message = "The status not 2xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_3xx_status(self, message: str):
        """Assert response in range 3xx status code"""
        if not 300 <= self.response.status_code < 400:
            message = "The status not 3xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_4xx_status(self, message: str):
        """Assert response in range 4xx status code"""
        if not 400 <= self.response.status_code < 500:
            message = "The status not 4xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_is_5xx_status(self, message: str):
        """Assert response in range 5xx status code"""
        if not 500 <= self.response.status_code < 600:
            message = "The status not 5xx"
            raise AssertionError(message)
        else:
            print(message)

    def assert_has_content(self, message: str):
        """Assert response has content"""
        if self.response.content:
            print(message, f"The content was => {self.response.content}")
        else:
            message = "There's no content in the body"  # pragma: no cover
            raise AssertionError(message)

    def assert_has_json(self, message: str):
        """Assert response has JSON body"""
        if self.response.json:
            print(message, f"The JSON body was => {self.response.json}")
        else:
            message = "The request has no JSON object"  # pragma: no cover
            raise AssertionError(message)

    def assert_has_text(self, message: str):
        """Assert response has text"""
        if self.response.text:
            print(message, f"The request has text => {self.response.text}")
        else:
            message = "The request has no text object"  # pragma: no cover
            raise AssertionError(message)

    def assert_status_code_in(self, status_code: int, message: str):
        """Assert response status code in range expected result"""
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result in expected_result:
            return print(message)
        else:
            message = "The expected status code didn't match with actual result"  # pragma: no cover
            raise AssertionError(message)

    def assert_status_code_not_in(self, status_code: int, message: str):
        """Assert response status code not in range expected result"""
        expected_result = [str(code) for code in status_code]
        actual_result = str(self.response.status_code)
        if actual_result not in expected_result:
            return print(message)
        else:
            message = (
                "The expected status code (actually) did matched with actual result"  # pragma: no cover
            )
            raise AssertionError(message)

    def assert_json_to_equal(self, obj, message: str):
        """Assert JSON response equal to expected result"""
        response_data = self.response.json()
        dumps = json.dumps(response_data, sort_keys=False)
        loads = json.loads(dumps)
        if loads == obj:
            return print(message)
        else:
            message = "There's no object that match"
            raise AssertionError(message)

    def assert_content_to_equal(self, obj, message: str):
        if self.response.content == obj:
            return print(message)
        else:
            message = "There's no content that match"
            raise AssertionError(message)

    def assert_response_time(self, duration: int, message: str):
        """Assert response time is less with set of duration"""
        if self.response.elapsed.total_seconds() <= duration:
            return print(message)
        else:
            message = "The duration exceeds the limit"
            raise AssertionError(message)

    def assert_text_to_equal(self, obj: Optional[bytes], message: str):
        if self.response.text:
            return print(isinstance(obj, str)), message
        else:
            message = f"Str type doesn't match with {obj}"  # pragma: no cover
            raise AssertionError(message)

    def assert_dict_to_equal(self, obj: dict, message: str):
        if self.response.json:
            return print(isinstance(obj, dict)), message
        else:
            message = f"Dict type doesn't match with {obj}"  # pragma: no cover
            raise AssertionError(message)

    def assert_response_time_less(self, message: str):
        """Assert response time is less with maximum duration"""
        # this one actually inspired from postman
        # collection test script about getting response
        # whenever calling an API
        max_duration = 200
        if self.response.elapsed.total_seconds() <= max_duration:
            return print(message)
        else:
            message = "The duration exceeds the limit"  # pragma: no cover
            raise AssertionError(message)

    def assert_expected_to_fail(self, message: str):
        """Assert request expected to be failed"""
        if self.response.status_code in [200, 201]:
            return print(message)
        else:
            message = "Expected to be failed, but got success instead"
            raise AssertionError(message)

    def assert_content_length(self, message: str = None):
        """Assert response has content-length header"""
        if message is None:
            if self.response.headers["Content-Length"]:
                message = "Request have content-length"
                return print(message)
            else:
                message = "Request doesn't have content-length"
                raise AssertionError(message)
        else:
            return print(message)

    def assert_tls_secure(self, message: str = None):
        """Assert request was TLS secure or invalid"""
        if message is None:
            if self.url.startswith("https://"):
                message = "Your connection to the request was secure"
                return print(message)
            if self.url.startswith("http://"):
                message = "Your connection to the request wasn't secure"
                return print(message)
        else:
            return print(message)

    def assert_keys_in_response(self, keys, message: str = None):
        """Assert request if keys has in JSON response"""
        key_in_response = self.response.json()
        expected_keys = keys_in_dict(lookup=key_in_response, keys=keys)
        if not expected_keys:
            message = "There's no any key in JSON response"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_xpath_data(self, query_path: str, expected_data: Any, message: str):
        """Assert that expected data contains in XPATH response"""
        # this assertion came up after reading built-in
        # assertion in Assertible documentation, please read here:
        # https://assertible.com/docs/guide/assertions#assert-xml/html-data
        response_content = self.response.content
        parsing = html.fromstring(response_content)
        find_element = parsing.xpath(query_path)
        if find_element != expected_data:
            message = "Data not equals or not found within XPATH response"
            raise AssertionError(message)
        else:
            return print(message)

    def assert_link_data(self, expected_values: str = None, message: str = None):
        """Assert for checking href link attribute in HTTP response"""
        response_content = self.response.content
        parsing = html.fromstring(response_content)
        for find_element in parsing.xpath("//a/@href"):
            if (
                find_element.startswith(("https", "http"))
                and find_element not in expected_values
            ):
                message = "Link not equals or not found within content response"
                raise AssertionError(message)
            else:
                return print(message)

    # im actually still unsure about implementing
    # HTTP verb methods to send a request, whether
    # it only use staticmethod or using normal method
    # and most likely it will be refactoring
    # the entire of codebase, so it kinda split out
    # between prepare request and final send request.
    # The major concern in here most likely there were
    # some flaws whenever use staticmethod when send
    # request using HTTP verb method. Since, this Assert
    # class is inherited from Http base class in other
    # module, basically it must be initiate all object
    # attributes (its redundant i think). Whereas
    # when using staticmethod for send a request, there
    # are some advantageous such as: easier to use
    # due certainty that only standalone method can be
    # use for performing 1 action or wants to keep all
    # information without override other object attributes
    # that comes from Http base class

    @staticmethod
    def get(url, headers, **kwargs):
        """interface for send HTTP request with performing ``GET`` method"""
        return Assert(method="GET", url=url, headers=headers, **kwargs)

    @staticmethod
    def post(url, headers, **kwargs):
        """interface for send HTTP request with performing ``POST`` method"""
        return Assert(method="POST", url=url, headers=headers, **kwargs)

    @staticmethod
    def delete(url, headers, **kwargs):
        """interface for send HTTP request with performing ``DELETE`` method"""
        return Assert(method="DELETE", url=url, headers=headers, **kwargs)

    @staticmethod
    def put(url, headers, **kwargs):
        """interface for send HTTP request with performing ``PUT`` method"""
        return Assert(method="PUT", url=url, headers=headers, **kwargs)

    @staticmethod
    def patch(url, headers, **kwargs):
        """interface for send HTTP request with performing ``PATCH`` method"""
        return Assert(method="PATCH", url=url, headers=headers, **kwargs)

    # TODO: write assertion for validating JSON body
