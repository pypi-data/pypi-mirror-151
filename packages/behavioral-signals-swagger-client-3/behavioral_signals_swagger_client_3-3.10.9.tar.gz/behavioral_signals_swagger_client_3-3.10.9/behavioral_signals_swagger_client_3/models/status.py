# coding: utf-8

"""
    Oliver API

    Oliver API service  # noqa: E501

    OpenAPI spec version: 3.10.9
    Contact: api@behavioralsignals.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Status(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'response': 'int',
        'detail': 'str'
    }

    attribute_map = {
        'response': 'response',
        'detail': 'detail'
    }

    def __init__(self, response=None, detail=None):  # noqa: E501
        """Status - a model defined in Swagger"""  # noqa: E501
        self._response = None
        self._detail = None
        self.discriminator = None
        self.response = response
        if detail is not None:
            self.detail = detail

    @property
    def response(self):
        """Gets the response of this Status.  # noqa: E501

        Code response of service status  # noqa: E501

        :return: The response of this Status.  # noqa: E501
        :rtype: int
        """
        return self._response

    @response.setter
    def response(self, response):
        """Sets the response of this Status.

        Code response of service status  # noqa: E501

        :param response: The response of this Status.  # noqa: E501
        :type: int
        """
        if response is None:
            raise ValueError("Invalid value for `response`, must not be `None`")  # noqa: E501

        self._response = response

    @property
    def detail(self):
        """Gets the detail of this Status.  # noqa: E501

        Human readable status  # noqa: E501

        :return: The detail of this Status.  # noqa: E501
        :rtype: str
        """
        return self._detail

    @detail.setter
    def detail(self, detail):
        """Sets the detail of this Status.

        Human readable status  # noqa: E501

        :param detail: The detail of this Status.  # noqa: E501
        :type: str
        """

        self._detail = detail

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(Status, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, Status):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
