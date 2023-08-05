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

class ResultJSONASR(object):
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
        'words': 'list[ResultJSONASRWords]',
        'predictions': 'list[ResultJSONASRPredictions]'
    }

    attribute_map = {
        'words': 'words',
        'predictions': 'predictions'
    }

    def __init__(self, words=None, predictions=None):  # noqa: E501
        """ResultJSONASR - a model defined in Swagger"""  # noqa: E501
        self._words = None
        self._predictions = None
        self.discriminator = None
        self.words = words
        if predictions is not None:
            self.predictions = predictions

    @property
    def words(self):
        """Gets the words of this ResultJSONASR.  # noqa: E501

        Contains transcribed word list  # noqa: E501

        :return: The words of this ResultJSONASR.  # noqa: E501
        :rtype: list[ResultJSONASRWords]
        """
        return self._words

    @words.setter
    def words(self, words):
        """Sets the words of this ResultJSONASR.

        Contains transcribed word list  # noqa: E501

        :param words: The words of this ResultJSONASR.  # noqa: E501
        :type: list[ResultJSONASRWords]
        """
        if words is None:
            raise ValueError("Invalid value for `words`, must not be `None`")  # noqa: E501

        self._words = words

    @property
    def predictions(self):
        """Gets the predictions of this ResultJSONASR.  # noqa: E501

        Predictions based on associated task  # noqa: E501

        :return: The predictions of this ResultJSONASR.  # noqa: E501
        :rtype: list[ResultJSONASRPredictions]
        """
        return self._predictions

    @predictions.setter
    def predictions(self, predictions):
        """Sets the predictions of this ResultJSONASR.

        Predictions based on associated task  # noqa: E501

        :param predictions: The predictions of this ResultJSONASR.  # noqa: E501
        :type: list[ResultJSONASRPredictions]
        """

        self._predictions = predictions

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
        if issubclass(ResultJSONASR, dict):
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
        if not isinstance(other, ResultJSONASR):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
