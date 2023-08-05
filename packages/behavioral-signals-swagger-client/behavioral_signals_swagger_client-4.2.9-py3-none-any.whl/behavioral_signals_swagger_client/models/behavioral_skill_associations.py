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

class BehavioralSkillAssociations(object):
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
        'id': 'BehavioralSkillId',
        'agents': 'list[SpeakerId]',
        'customers': 'list[SpeakerId]',
        'portfolio_id': 'PortfolioId'
    }

    attribute_map = {
        'id': 'id',
        'agents': 'agents',
        'customers': 'customers',
        'portfolio_id': 'portfolioId'
    }

    def __init__(self, id=None, agents=None, customers=None, portfolio_id=None):  # noqa: E501
        """BehavioralSkillAssociations - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._agents = None
        self._customers = None
        self._portfolio_id = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if agents is not None:
            self.agents = agents
        if customers is not None:
            self.customers = customers
        if portfolio_id is not None:
            self.portfolio_id = portfolio_id

    @property
    def id(self):
        """Gets the id of this BehavioralSkillAssociations.  # noqa: E501


        :return: The id of this BehavioralSkillAssociations.  # noqa: E501
        :rtype: BehavioralSkillId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BehavioralSkillAssociations.


        :param id: The id of this BehavioralSkillAssociations.  # noqa: E501
        :type: BehavioralSkillId
        """

        self._id = id

    @property
    def agents(self):
        """Gets the agents of this BehavioralSkillAssociations.  # noqa: E501

        Array of behavioral skill agent ids  # noqa: E501

        :return: The agents of this BehavioralSkillAssociations.  # noqa: E501
        :rtype: list[SpeakerId]
        """
        return self._agents

    @agents.setter
    def agents(self, agents):
        """Sets the agents of this BehavioralSkillAssociations.

        Array of behavioral skill agent ids  # noqa: E501

        :param agents: The agents of this BehavioralSkillAssociations.  # noqa: E501
        :type: list[SpeakerId]
        """

        self._agents = agents

    @property
    def customers(self):
        """Gets the customers of this BehavioralSkillAssociations.  # noqa: E501

        Array of behavioral skill customer ids  # noqa: E501

        :return: The customers of this BehavioralSkillAssociations.  # noqa: E501
        :rtype: list[SpeakerId]
        """
        return self._customers

    @customers.setter
    def customers(self, customers):
        """Sets the customers of this BehavioralSkillAssociations.

        Array of behavioral skill customer ids  # noqa: E501

        :param customers: The customers of this BehavioralSkillAssociations.  # noqa: E501
        :type: list[SpeakerId]
        """

        self._customers = customers

    @property
    def portfolio_id(self):
        """Gets the portfolio_id of this BehavioralSkillAssociations.  # noqa: E501


        :return: The portfolio_id of this BehavioralSkillAssociations.  # noqa: E501
        :rtype: PortfolioId
        """
        return self._portfolio_id

    @portfolio_id.setter
    def portfolio_id(self, portfolio_id):
        """Sets the portfolio_id of this BehavioralSkillAssociations.


        :param portfolio_id: The portfolio_id of this BehavioralSkillAssociations.  # noqa: E501
        :type: PortfolioId
        """

        self._portfolio_id = portfolio_id

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
        if issubclass(BehavioralSkillAssociations, dict):
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
        if not isinstance(other, BehavioralSkillAssociations):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
