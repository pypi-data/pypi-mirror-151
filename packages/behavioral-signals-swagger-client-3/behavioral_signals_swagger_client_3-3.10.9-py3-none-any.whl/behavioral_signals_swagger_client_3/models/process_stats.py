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

class ProcessStats(object):
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
        'cid': 'int',
        'pid': 'int',
        'status': 'int',
        'total': 'float',
        'pending': 'float',
        'processing': 'float',
        'retrying': 'float',
        'retries': 'int',
        'extended_timers': 'list[float]'
    }

    attribute_map = {
        'cid': 'cid',
        'pid': 'pid',
        'status': 'status',
        'total': 'total',
        'pending': 'pending',
        'processing': 'processing',
        'retrying': 'retrying',
        'retries': 'retries',
        'extended_timers': 'extendedTimers'
    }

    def __init__(self, cid=None, pid=None, status=None, total=None, pending=None, processing=None, retrying=None, retries=None, extended_timers=None):  # noqa: E501
        """ProcessStats - a model defined in Swagger"""  # noqa: E501
        self._cid = None
        self._pid = None
        self._status = None
        self._total = None
        self._pending = None
        self._processing = None
        self._retrying = None
        self._retries = None
        self._extended_timers = None
        self.discriminator = None
        if cid is not None:
            self.cid = cid
        self.pid = pid
        if status is not None:
            self.status = status
        if total is not None:
            self.total = total
        if pending is not None:
            self.pending = pending
        if processing is not None:
            self.processing = processing
        if retrying is not None:
            self.retrying = retrying
        if retries is not None:
            self.retries = retries
        if extended_timers is not None:
            self.extended_timers = extended_timers

    @property
    def cid(self):
        """Gets the cid of this ProcessStats.  # noqa: E501

        Client ID that requested the processing  # noqa: E501

        :return: The cid of this ProcessStats.  # noqa: E501
        :rtype: int
        """
        return self._cid

    @cid.setter
    def cid(self, cid):
        """Sets the cid of this ProcessStats.

        Client ID that requested the processing  # noqa: E501

        :param cid: The cid of this ProcessStats.  # noqa: E501
        :type: int
        """

        self._cid = cid

    @property
    def pid(self):
        """Gets the pid of this ProcessStats.  # noqa: E501

        Unique ID for the processing job  # noqa: E501

        :return: The pid of this ProcessStats.  # noqa: E501
        :rtype: int
        """
        return self._pid

    @pid.setter
    def pid(self, pid):
        """Sets the pid of this ProcessStats.

        Unique ID for the processing job  # noqa: E501

        :param pid: The pid of this ProcessStats.  # noqa: E501
        :type: int
        """
        if pid is None:
            raise ValueError("Invalid value for `pid`, must not be `None`")  # noqa: E501

        self._pid = pid

    @property
    def status(self):
        """Gets the status of this ProcessStats.  # noqa: E501

        Shows the processing state of the job. Status is 0: pending, 1: processing, 2: completed, -1:failed, -2 aborted  # noqa: E501

        :return: The status of this ProcessStats.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this ProcessStats.

        Shows the processing state of the job. Status is 0: pending, 1: processing, 2: completed, -1:failed, -2 aborted  # noqa: E501

        :param status: The status of this ProcessStats.  # noqa: E501
        :type: int
        """

        self._status = status

    @property
    def total(self):
        """Gets the total of this ProcessStats.  # noqa: E501

        The time from the moment inserted in the queue till reaching final state  # noqa: E501

        :return: The total of this ProcessStats.  # noqa: E501
        :rtype: float
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ProcessStats.

        The time from the moment inserted in the queue till reaching final state  # noqa: E501

        :param total: The total of this ProcessStats.  # noqa: E501
        :type: float
        """

        self._total = total

    @property
    def pending(self):
        """Gets the pending of this ProcessStats.  # noqa: E501

        Total time the audio was on the queue  # noqa: E501

        :return: The pending of this ProcessStats.  # noqa: E501
        :rtype: float
        """
        return self._pending

    @pending.setter
    def pending(self, pending):
        """Sets the pending of this ProcessStats.

        Total time the audio was on the queue  # noqa: E501

        :param pending: The pending of this ProcessStats.  # noqa: E501
        :type: float
        """

        self._pending = pending

    @property
    def processing(self):
        """Gets the processing of this ProcessStats.  # noqa: E501

        Total time the audio was in processing state  # noqa: E501

        :return: The processing of this ProcessStats.  # noqa: E501
        :rtype: float
        """
        return self._processing

    @processing.setter
    def processing(self, processing):
        """Sets the processing of this ProcessStats.

        Total time the audio was in processing state  # noqa: E501

        :param processing: The processing of this ProcessStats.  # noqa: E501
        :type: float
        """

        self._processing = processing

    @property
    def retrying(self):
        """Gets the retrying of this ProcessStats.  # noqa: E501

        Total time the audio was in failed state  # noqa: E501

        :return: The retrying of this ProcessStats.  # noqa: E501
        :rtype: float
        """
        return self._retrying

    @retrying.setter
    def retrying(self, retrying):
        """Sets the retrying of this ProcessStats.

        Total time the audio was in failed state  # noqa: E501

        :param retrying: The retrying of this ProcessStats.  # noqa: E501
        :type: float
        """

        self._retrying = retrying

    @property
    def retries(self):
        """Gets the retries of this ProcessStats.  # noqa: E501

        Number of retries before transiting to a final state  # noqa: E501

        :return: The retries of this ProcessStats.  # noqa: E501
        :rtype: int
        """
        return self._retries

    @retries.setter
    def retries(self, retries):
        """Sets the retries of this ProcessStats.

        Number of retries before transiting to a final state  # noqa: E501

        :param retries: The retries of this ProcessStats.  # noqa: E501
        :type: int
        """

        self._retries = retries

    @property
    def extended_timers(self):
        """Gets the extended_timers of this ProcessStats.  # noqa: E501

        Extended Timers  # noqa: E501

        :return: The extended_timers of this ProcessStats.  # noqa: E501
        :rtype: list[float]
        """
        return self._extended_timers

    @extended_timers.setter
    def extended_timers(self, extended_timers):
        """Sets the extended_timers of this ProcessStats.

        Extended Timers  # noqa: E501

        :param extended_timers: The extended_timers of this ProcessStats.  # noqa: E501
        :type: list[float]
        """

        self._extended_timers = extended_timers

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
        if issubclass(ProcessStats, dict):
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
        if not isinstance(other, ProcessStats):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
