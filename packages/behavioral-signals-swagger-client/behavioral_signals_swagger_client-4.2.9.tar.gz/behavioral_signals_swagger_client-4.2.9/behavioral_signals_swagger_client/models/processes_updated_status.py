# coding: utf-8

"""
    Oliver API

    Oliver API service  # noqa: E501

    OpenAPI spec version: 4.2.9
    Contact: api@behavioralsignals.com
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ProcessesUpdatedStatus(object):
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
        'action': 'str',
        'total': 'int',
        'updated': 'int',
        'failed': 'list[ProcessUpdatedStatus]'
    }

    attribute_map = {
        'action': 'action',
        'total': 'total',
        'updated': 'updated',
        'failed': 'failed'
    }

    def __init__(self, action=None, total=None, updated=None, failed=None):  # noqa: E501
        """ProcessesUpdatedStatus - a model defined in Swagger"""  # noqa: E501
        self._action = None
        self._total = None
        self._updated = None
        self._failed = None
        self.discriminator = None
        if action is not None:
            self.action = action
        if total is not None:
            self.total = total
        if updated is not None:
            self.updated = updated
        if failed is not None:
            self.failed = failed

    @property
    def action(self):
        """Gets the action of this ProcessesUpdatedStatus.  # noqa: E501


        :return: The action of this ProcessesUpdatedStatus.  # noqa: E501
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """Sets the action of this ProcessesUpdatedStatus.


        :param action: The action of this ProcessesUpdatedStatus.  # noqa: E501
        :type: str
        """

        self._action = action

    @property
    def total(self):
        """Gets the total of this ProcessesUpdatedStatus.  # noqa: E501


        :return: The total of this ProcessesUpdatedStatus.  # noqa: E501
        :rtype: int
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this ProcessesUpdatedStatus.


        :param total: The total of this ProcessesUpdatedStatus.  # noqa: E501
        :type: int
        """

        self._total = total

    @property
    def updated(self):
        """Gets the updated of this ProcessesUpdatedStatus.  # noqa: E501


        :return: The updated of this ProcessesUpdatedStatus.  # noqa: E501
        :rtype: int
        """
        return self._updated

    @updated.setter
    def updated(self, updated):
        """Sets the updated of this ProcessesUpdatedStatus.


        :param updated: The updated of this ProcessesUpdatedStatus.  # noqa: E501
        :type: int
        """

        self._updated = updated

    @property
    def failed(self):
        """Gets the failed of this ProcessesUpdatedStatus.  # noqa: E501


        :return: The failed of this ProcessesUpdatedStatus.  # noqa: E501
        :rtype: list[ProcessUpdatedStatus]
        """
        return self._failed

    @failed.setter
    def failed(self, failed):
        """Sets the failed of this ProcessesUpdatedStatus.


        :param failed: The failed of this ProcessesUpdatedStatus.  # noqa: E501
        :type: list[ProcessUpdatedStatus]
        """

        self._failed = failed

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
        if issubclass(ProcessesUpdatedStatus, dict):
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
        if not isinstance(other, ProcessesUpdatedStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
