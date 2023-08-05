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

class ResultJSONFramesPoliteness(object):
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
        'framelevel': 'float',
        'uptonow': 'float'
    }

    attribute_map = {
        'framelevel': 'framelevel',
        'uptonow': 'uptonow'
    }

    def __init__(self, framelevel=None, uptonow=None):  # noqa: E501
        """ResultJSONFramesPoliteness - a model defined in Swagger"""  # noqa: E501
        self._framelevel = None
        self._uptonow = None
        self.discriminator = None
        if framelevel is not None:
            self.framelevel = framelevel
        if uptonow is not None:
            self.uptonow = uptonow

    @property
    def framelevel(self):
        """Gets the framelevel of this ResultJSONFramesPoliteness.  # noqa: E501

        Result of current frame  # noqa: E501

        :return: The framelevel of this ResultJSONFramesPoliteness.  # noqa: E501
        :rtype: float
        """
        return self._framelevel

    @framelevel.setter
    def framelevel(self, framelevel):
        """Sets the framelevel of this ResultJSONFramesPoliteness.

        Result of current frame  # noqa: E501

        :param framelevel: The framelevel of this ResultJSONFramesPoliteness.  # noqa: E501
        :type: float
        """

        self._framelevel = framelevel

    @property
    def uptonow(self):
        """Gets the uptonow of this ResultJSONFramesPoliteness.  # noqa: E501

        Decision up to current frame  # noqa: E501

        :return: The uptonow of this ResultJSONFramesPoliteness.  # noqa: E501
        :rtype: float
        """
        return self._uptonow

    @uptonow.setter
    def uptonow(self, uptonow):
        """Sets the uptonow of this ResultJSONFramesPoliteness.

        Decision up to current frame  # noqa: E501

        :param uptonow: The uptonow of this ResultJSONFramesPoliteness.  # noqa: E501
        :type: float
        """

        self._uptonow = uptonow

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
        if issubclass(ResultJSONFramesPoliteness, dict):
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
        if not isinstance(other, ResultJSONFramesPoliteness):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
