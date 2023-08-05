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

class Token(object):
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
        'token': 'str',
        'role': 'str',
        'cid': 'int',
        'status': 'int'
    }

    attribute_map = {
        'token': 'token',
        'role': 'role',
        'cid': 'cid',
        'status': 'status'
    }

    def __init__(self, token=None, role=None, cid=None, status=None):  # noqa: E501
        """Token - a model defined in Swagger"""  # noqa: E501
        self._token = None
        self._role = None
        self._cid = None
        self._status = None
        self.discriminator = None
        self.token = token
        self.role = role
        self.cid = cid
        self.status = status

    @property
    def token(self):
        """Gets the token of this Token.  # noqa: E501

        The token hash string  # noqa: E501

        :return: The token of this Token.  # noqa: E501
        :rtype: str
        """
        return self._token

    @token.setter
    def token(self, token):
        """Sets the token of this Token.

        The token hash string  # noqa: E501

        :param token: The token of this Token.  # noqa: E501
        :type: str
        """
        if token is None:
            raise ValueError("Invalid value for `token`, must not be `None`")  # noqa: E501

        self._token = token

    @property
    def role(self):
        """Gets the role of this Token.  # noqa: E501

        The role can be user/administrator  # noqa: E501

        :return: The role of this Token.  # noqa: E501
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role):
        """Sets the role of this Token.

        The role can be user/administrator  # noqa: E501

        :param role: The role of this Token.  # noqa: E501
        :type: str
        """
        if role is None:
            raise ValueError("Invalid value for `role`, must not be `None`")  # noqa: E501

        self._role = role

    @property
    def cid(self):
        """Gets the cid of this Token.  # noqa: E501

        the client id that will be associated with this token  # noqa: E501

        :return: The cid of this Token.  # noqa: E501
        :rtype: int
        """
        return self._cid

    @cid.setter
    def cid(self, cid):
        """Sets the cid of this Token.

        the client id that will be associated with this token  # noqa: E501

        :param cid: The cid of this Token.  # noqa: E501
        :type: int
        """
        if cid is None:
            raise ValueError("Invalid value for `cid`, must not be `None`")  # noqa: E501

        self._cid = cid

    @property
    def status(self):
        """Gets the status of this Token.  # noqa: E501

        The status can be -1/0/1 expired/disabled/active  # noqa: E501

        :return: The status of this Token.  # noqa: E501
        :rtype: int
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Token.

        The status can be -1/0/1 expired/disabled/active  # noqa: E501

        :param status: The status of this Token.  # noqa: E501
        :type: int
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

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
        if issubclass(Token, dict):
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
        if not isinstance(other, Token):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
