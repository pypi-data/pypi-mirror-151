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

class ResultJSONDiarizationDiarization(object):
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
        'c': 'float',
        'st': 'float',
        'et': 'float',
        'p': 'int',
        'm': 'str'
    }

    attribute_map = {
        'c': 'c',
        'st': 'st',
        'et': 'et',
        'p': 'p',
        'm': 'm'
    }

    def __init__(self, c=None, st=None, et=None, p=None, m=None):  # noqa: E501
        """ResultJSONDiarizationDiarization - a model defined in Swagger"""  # noqa: E501
        self._c = None
        self._st = None
        self._et = None
        self._p = None
        self._m = None
        self.discriminator = None
        if c is not None:
            self.c = c
        if st is not None:
            self.st = st
        if et is not None:
            self.et = et
        if p is not None:
            self.p = p
        if m is not None:
            self.m = m

    @property
    def c(self):
        """Gets the c of this ResultJSONDiarizationDiarization.  # noqa: E501

        Confidence  # noqa: E501

        :return: The c of this ResultJSONDiarizationDiarization.  # noqa: E501
        :rtype: float
        """
        return self._c

    @c.setter
    def c(self, c):
        """Sets the c of this ResultJSONDiarizationDiarization.

        Confidence  # noqa: E501

        :param c: The c of this ResultJSONDiarizationDiarization.  # noqa: E501
        :type: float
        """

        self._c = c

    @property
    def st(self):
        """Gets the st of this ResultJSONDiarizationDiarization.  # noqa: E501

        The start time of the word in seconds from begining  # noqa: E501

        :return: The st of this ResultJSONDiarizationDiarization.  # noqa: E501
        :rtype: float
        """
        return self._st

    @st.setter
    def st(self, st):
        """Sets the st of this ResultJSONDiarizationDiarization.

        The start time of the word in seconds from begining  # noqa: E501

        :param st: The st of this ResultJSONDiarizationDiarization.  # noqa: E501
        :type: float
        """

        self._st = st

    @property
    def et(self):
        """Gets the et of this ResultJSONDiarizationDiarization.  # noqa: E501

        The end time of the word in seconds from begining  # noqa: E501

        :return: The et of this ResultJSONDiarizationDiarization.  # noqa: E501
        :rtype: float
        """
        return self._et

    @et.setter
    def et(self, et):
        """Sets the et of this ResultJSONDiarizationDiarization.

        The end time of the word in seconds from begining  # noqa: E501

        :param et: The et of this ResultJSONDiarizationDiarization.  # noqa: E501
        :type: float
        """

        self._et = et

    @property
    def p(self):
        """Gets the p of this ResultJSONDiarizationDiarization.  # noqa: E501

        Index starting from zero  # noqa: E501

        :return: The p of this ResultJSONDiarizationDiarization.  # noqa: E501
        :rtype: int
        """
        return self._p

    @p.setter
    def p(self, p):
        """Sets the p of this ResultJSONDiarizationDiarization.

        Index starting from zero  # noqa: E501

        :param p: The p of this ResultJSONDiarizationDiarization.  # noqa: E501
        :type: int
        """

        self._p = p

    @property
    def m(self):
        """Gets the m of this ResultJSONDiarizationDiarization.  # noqa: E501

        Flag  # noqa: E501

        :return: The m of this ResultJSONDiarizationDiarization.  # noqa: E501
        :rtype: str
        """
        return self._m

    @m.setter
    def m(self, m):
        """Sets the m of this ResultJSONDiarizationDiarization.

        Flag  # noqa: E501

        :param m: The m of this ResultJSONDiarizationDiarization.  # noqa: E501
        :type: str
        """

        self._m = m

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
        if issubclass(ResultJSONDiarizationDiarization, dict):
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
        if not isinstance(other, ResultJSONDiarizationDiarization):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
