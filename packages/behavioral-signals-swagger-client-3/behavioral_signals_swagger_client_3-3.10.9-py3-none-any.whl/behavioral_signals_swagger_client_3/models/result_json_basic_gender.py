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

class ResultJSONBasicGender(object):
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
        'agent': 'int',
        'customer': 'int',
        'speaker1': 'int',
        'speaker2': 'int',
        'speaker3': 'int',
        'speaker4': 'int',
        'speaker5': 'int',
        'speaker6': 'int',
        'speaker7': 'int',
        'speaker8': 'int',
        'speaker9': 'int'
    }

    attribute_map = {
        'agent': 'agent',
        'customer': 'customer',
        'speaker1': 'speaker1',
        'speaker2': 'speaker2',
        'speaker3': 'speaker3',
        'speaker4': 'speaker4',
        'speaker5': 'speaker5',
        'speaker6': 'speaker6',
        'speaker7': 'speaker7',
        'speaker8': 'speaker8',
        'speaker9': 'speaker9'
    }

    def __init__(self, agent=None, customer=None, speaker1=None, speaker2=None, speaker3=None, speaker4=None, speaker5=None, speaker6=None, speaker7=None, speaker8=None, speaker9=None):  # noqa: E501
        """ResultJSONBasicGender - a model defined in Swagger"""  # noqa: E501
        self._agent = None
        self._customer = None
        self._speaker1 = None
        self._speaker2 = None
        self._speaker3 = None
        self._speaker4 = None
        self._speaker5 = None
        self._speaker6 = None
        self._speaker7 = None
        self._speaker8 = None
        self._speaker9 = None
        self.discriminator = None
        if agent is not None:
            self.agent = agent
        if customer is not None:
            self.customer = customer
        if speaker1 is not None:
            self.speaker1 = speaker1
        if speaker2 is not None:
            self.speaker2 = speaker2
        if speaker3 is not None:
            self.speaker3 = speaker3
        if speaker4 is not None:
            self.speaker4 = speaker4
        if speaker5 is not None:
            self.speaker5 = speaker5
        if speaker6 is not None:
            self.speaker6 = speaker6
        if speaker7 is not None:
            self.speaker7 = speaker7
        if speaker8 is not None:
            self.speaker8 = speaker8
        if speaker9 is not None:
            self.speaker9 = speaker9

    @property
    def agent(self):
        """Gets the agent of this ResultJSONBasicGender.  # noqa: E501

        Agent gender index: 1=female, 2=male  # noqa: E501

        :return: The agent of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """Sets the agent of this ResultJSONBasicGender.

        Agent gender index: 1=female, 2=male  # noqa: E501

        :param agent: The agent of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._agent = agent

    @property
    def customer(self):
        """Gets the customer of this ResultJSONBasicGender.  # noqa: E501

        Customer gender index: 1=female, 2=male  # noqa: E501

        :return: The customer of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._customer

    @customer.setter
    def customer(self, customer):
        """Sets the customer of this ResultJSONBasicGender.

        Customer gender index: 1=female, 2=male  # noqa: E501

        :param customer: The customer of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._customer = customer

    @property
    def speaker1(self):
        """Gets the speaker1 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker1 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker1

    @speaker1.setter
    def speaker1(self, speaker1):
        """Sets the speaker1 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker1: The speaker1 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker1 = speaker1

    @property
    def speaker2(self):
        """Gets the speaker2 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker2 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker2

    @speaker2.setter
    def speaker2(self, speaker2):
        """Sets the speaker2 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker2: The speaker2 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker2 = speaker2

    @property
    def speaker3(self):
        """Gets the speaker3 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker3 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker3

    @speaker3.setter
    def speaker3(self, speaker3):
        """Sets the speaker3 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker3: The speaker3 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker3 = speaker3

    @property
    def speaker4(self):
        """Gets the speaker4 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker4 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker4

    @speaker4.setter
    def speaker4(self, speaker4):
        """Sets the speaker4 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker4: The speaker4 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker4 = speaker4

    @property
    def speaker5(self):
        """Gets the speaker5 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker5 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker5

    @speaker5.setter
    def speaker5(self, speaker5):
        """Sets the speaker5 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker5: The speaker5 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker5 = speaker5

    @property
    def speaker6(self):
        """Gets the speaker6 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker6 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker6

    @speaker6.setter
    def speaker6(self, speaker6):
        """Sets the speaker6 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker6: The speaker6 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker6 = speaker6

    @property
    def speaker7(self):
        """Gets the speaker7 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker7 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker7

    @speaker7.setter
    def speaker7(self, speaker7):
        """Sets the speaker7 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker7: The speaker7 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker7 = speaker7

    @property
    def speaker8(self):
        """Gets the speaker8 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker8 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker8

    @speaker8.setter
    def speaker8(self, speaker8):
        """Sets the speaker8 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker8: The speaker8 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker8 = speaker8

    @property
    def speaker9(self):
        """Gets the speaker9 of this ResultJSONBasicGender.  # noqa: E501

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :return: The speaker9 of this ResultJSONBasicGender.  # noqa: E501
        :rtype: int
        """
        return self._speaker9

    @speaker9.setter
    def speaker9(self, speaker9):
        """Sets the speaker9 of this ResultJSONBasicGender.

        Speaker gender index: 1=female, 2=male  # noqa: E501

        :param speaker9: The speaker9 of this ResultJSONBasicGender.  # noqa: E501
        :type: int
        """

        self._speaker9 = speaker9

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
        if issubclass(ResultJSONBasicGender, dict):
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
        if not isinstance(other, ResultJSONBasicGender):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
