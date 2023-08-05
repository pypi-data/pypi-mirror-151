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

class PaginationResponse(object):
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
        'total_items': 'int',
        'total_pages': 'int',
        'current_page': 'int'
    }

    attribute_map = {
        'total_items': 'totalItems',
        'total_pages': 'totalPages',
        'current_page': 'currentPage'
    }

    def __init__(self, total_items=None, total_pages=None, current_page=None):  # noqa: E501
        """PaginationResponse - a model defined in Swagger"""  # noqa: E501
        self._total_items = None
        self._total_pages = None
        self._current_page = None
        self.discriminator = None
        if total_items is not None:
            self.total_items = total_items
        if total_pages is not None:
            self.total_pages = total_pages
        if current_page is not None:
            self.current_page = current_page

    @property
    def total_items(self):
        """Gets the total_items of this PaginationResponse.  # noqa: E501


        :return: The total_items of this PaginationResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_items

    @total_items.setter
    def total_items(self, total_items):
        """Sets the total_items of this PaginationResponse.


        :param total_items: The total_items of this PaginationResponse.  # noqa: E501
        :type: int
        """

        self._total_items = total_items

    @property
    def total_pages(self):
        """Gets the total_pages of this PaginationResponse.  # noqa: E501


        :return: The total_pages of this PaginationResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_pages

    @total_pages.setter
    def total_pages(self, total_pages):
        """Sets the total_pages of this PaginationResponse.


        :param total_pages: The total_pages of this PaginationResponse.  # noqa: E501
        :type: int
        """

        self._total_pages = total_pages

    @property
    def current_page(self):
        """Gets the current_page of this PaginationResponse.  # noqa: E501


        :return: The current_page of this PaginationResponse.  # noqa: E501
        :rtype: int
        """
        return self._current_page

    @current_page.setter
    def current_page(self, current_page):
        """Sets the current_page of this PaginationResponse.


        :param current_page: The current_page of this PaginationResponse.  # noqa: E501
        :type: int
        """

        self._current_page = current_page

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
        if issubclass(PaginationResponse, dict):
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
        if not isinstance(other, PaginationResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
