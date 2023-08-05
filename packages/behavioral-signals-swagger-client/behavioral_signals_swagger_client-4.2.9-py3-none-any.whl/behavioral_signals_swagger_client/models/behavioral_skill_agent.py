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

class BehavioralSkillAgent(object):
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
        'id': 'SpeakerId',
        'level': 'int'
    }

    attribute_map = {
        'id': 'id',
        'level': 'level'
    }

    def __init__(self, id=None, level=None):  # noqa: E501
        """BehavioralSkillAgent - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._level = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if level is not None:
            self.level = level

    @property
    def id(self):
        """Gets the id of this BehavioralSkillAgent.  # noqa: E501


        :return: The id of this BehavioralSkillAgent.  # noqa: E501
        :rtype: SpeakerId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BehavioralSkillAgent.


        :param id: The id of this BehavioralSkillAgent.  # noqa: E501
        :type: SpeakerId
        """

        self._id = id

    @property
    def level(self):
        """Gets the level of this BehavioralSkillAgent.  # noqa: E501


        :return: The level of this BehavioralSkillAgent.  # noqa: E501
        :rtype: int
        """
        return self._level

    @level.setter
    def level(self, level):
        """Sets the level of this BehavioralSkillAgent.


        :param level: The level of this BehavioralSkillAgent.  # noqa: E501
        :type: int
        """

        self._level = level

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
        if issubclass(BehavioralSkillAgent, dict):
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
        if not isinstance(other, BehavioralSkillAgent):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
