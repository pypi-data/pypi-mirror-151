# coding: utf-8

"""
    CLOUD API

    IONOS Enterprise-grade Infrastructure as a Service (IaaS) solutions can be managed through the Cloud API, in addition or as an alternative to the \"Data Center Designer\" (DCD) browser-based tool.    Both methods employ consistent concepts and features, deliver similar power and flexibility, and can be used to perform a multitude of management tasks, including adding servers, volumes, configuring networks, and so on.  # noqa: E501

    The version of the OpenAPI document: 6.0
    Generated by: https://openapi-generator.tech
"""


import pprint
import re  # noqa: F401

import six

from ionoscloud.configuration import Configuration


class ServerProperties(object):
    """NOTE: This class is auto generated by OpenAPI Generator.
    Ref: https://openapi-generator.tech

    Do not edit the class manually.
    """

    """
    Attributes:
      openapi_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    openapi_types = {

        'template_uuid': 'str',

        'name': 'str',

        'cores': 'int',

        'ram': 'int',

        'availability_zone': 'str',

        'vm_state': 'str',

        'boot_cdrom': 'ResourceReference',

        'boot_volume': 'ResourceReference',

        'cpu_family': 'str',

        'type': 'str',
    }

    attribute_map = {

        'template_uuid': 'templateUuid',

        'name': 'name',

        'cores': 'cores',

        'ram': 'ram',

        'availability_zone': 'availabilityZone',

        'vm_state': 'vmState',

        'boot_cdrom': 'bootCdrom',

        'boot_volume': 'bootVolume',

        'cpu_family': 'cpuFamily',

        'type': 'type',
    }

    def __init__(self, template_uuid=None, name=None, cores=None, ram=None, availability_zone=None, vm_state=None, boot_cdrom=None, boot_volume=None, cpu_family=None, type=None, local_vars_configuration=None):  # noqa: E501
        """ServerProperties - a model defined in OpenAPI"""  # noqa: E501
        if local_vars_configuration is None:
            local_vars_configuration = Configuration()
        self.local_vars_configuration = local_vars_configuration

        self._template_uuid = None
        self._name = None
        self._cores = None
        self._ram = None
        self._availability_zone = None
        self._vm_state = None
        self._boot_cdrom = None
        self._boot_volume = None
        self._cpu_family = None
        self._type = None
        self.discriminator = None

        if template_uuid is not None:
            self.template_uuid = template_uuid
        if name is not None:
            self.name = name
        self.cores = cores
        self.ram = ram
        if availability_zone is not None:
            self.availability_zone = availability_zone
        if vm_state is not None:
            self.vm_state = vm_state
        if boot_cdrom is not None:
            self.boot_cdrom = boot_cdrom
        if boot_volume is not None:
            self.boot_volume = boot_volume
        if cpu_family is not None:
            self.cpu_family = cpu_family
        if type is not None:
            self.type = type


    @property
    def template_uuid(self):
        """Gets the template_uuid of this ServerProperties.  # noqa: E501

        The ID of the template for creating a CUBE server; the available templates for CUBE servers can be found on the templates resource.  # noqa: E501

        :return: The template_uuid of this ServerProperties.  # noqa: E501
        :rtype: str
        """
        return self._template_uuid

    @template_uuid.setter
    def template_uuid(self, template_uuid):
        """Sets the template_uuid of this ServerProperties.

        The ID of the template for creating a CUBE server; the available templates for CUBE servers can be found on the templates resource.  # noqa: E501

        :param template_uuid: The template_uuid of this ServerProperties.  # noqa: E501
        :type template_uuid: str
        """

        self._template_uuid = template_uuid

    @property
    def name(self):
        """Gets the name of this ServerProperties.  # noqa: E501

        The name of the  resource.  # noqa: E501

        :return: The name of this ServerProperties.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this ServerProperties.

        The name of the  resource.  # noqa: E501

        :param name: The name of this ServerProperties.  # noqa: E501
        :type name: str
        """

        self._name = name

    @property
    def cores(self):
        """Gets the cores of this ServerProperties.  # noqa: E501

        The total number of cores for the server.  # noqa: E501

        :return: The cores of this ServerProperties.  # noqa: E501
        :rtype: int
        """
        return self._cores

    @cores.setter
    def cores(self, cores):
        """Sets the cores of this ServerProperties.

        The total number of cores for the server.  # noqa: E501

        :param cores: The cores of this ServerProperties.  # noqa: E501
        :type cores: int
        """
        if self.local_vars_configuration.client_side_validation and cores is None:  # noqa: E501
            raise ValueError("Invalid value for `cores`, must not be `None`")  # noqa: E501

        self._cores = cores

    @property
    def ram(self):
        """Gets the ram of this ServerProperties.  # noqa: E501

        The memory size for the server in MB, such as 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set ramHotPlug to TRUE then you must use a minimum of 1024 MB. If you set the RAM size more than 240GB, then ramHotPlug will be set to FALSE and can not be set to TRUE unless RAM size not set to less than 240GB.  # noqa: E501

        :return: The ram of this ServerProperties.  # noqa: E501
        :rtype: int
        """
        return self._ram

    @ram.setter
    def ram(self, ram):
        """Sets the ram of this ServerProperties.

        The memory size for the server in MB, such as 2048. Size must be specified in multiples of 256 MB with a minimum of 256 MB; however, if you set ramHotPlug to TRUE then you must use a minimum of 1024 MB. If you set the RAM size more than 240GB, then ramHotPlug will be set to FALSE and can not be set to TRUE unless RAM size not set to less than 240GB.  # noqa: E501

        :param ram: The ram of this ServerProperties.  # noqa: E501
        :type ram: int
        """
        if self.local_vars_configuration.client_side_validation and ram is None:  # noqa: E501
            raise ValueError("Invalid value for `ram`, must not be `None`")  # noqa: E501

        self._ram = ram

    @property
    def availability_zone(self):
        """Gets the availability_zone of this ServerProperties.  # noqa: E501

        The availability zone in which the server should be provisioned.  # noqa: E501

        :return: The availability_zone of this ServerProperties.  # noqa: E501
        :rtype: str
        """
        return self._availability_zone

    @availability_zone.setter
    def availability_zone(self, availability_zone):
        """Sets the availability_zone of this ServerProperties.

        The availability zone in which the server should be provisioned.  # noqa: E501

        :param availability_zone: The availability_zone of this ServerProperties.  # noqa: E501
        :type availability_zone: str
        """
        allowed_values = ["AUTO", "ZONE_1", "ZONE_2"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and availability_zone not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `availability_zone` ({0}), must be one of {1}"  # noqa: E501
                .format(availability_zone, allowed_values)
            )

        self._availability_zone = availability_zone

    @property
    def vm_state(self):
        """Gets the vm_state of this ServerProperties.  # noqa: E501

        Status of the virtual machine.  # noqa: E501

        :return: The vm_state of this ServerProperties.  # noqa: E501
        :rtype: str
        """
        return self._vm_state

    @vm_state.setter
    def vm_state(self, vm_state):
        """Sets the vm_state of this ServerProperties.

        Status of the virtual machine.  # noqa: E501

        :param vm_state: The vm_state of this ServerProperties.  # noqa: E501
        :type vm_state: str
        """
        allowed_values = ["NOSTATE", "RUNNING", "BLOCKED", "PAUSED", "SHUTDOWN", "SHUTOFF", "CRASHED", "SUSPENDED"]  # noqa: E501
        if self.local_vars_configuration.client_side_validation and vm_state not in allowed_values:  # noqa: E501
            raise ValueError(
                "Invalid value for `vm_state` ({0}), must be one of {1}"  # noqa: E501
                .format(vm_state, allowed_values)
            )

        self._vm_state = vm_state

    @property
    def boot_cdrom(self):
        """Gets the boot_cdrom of this ServerProperties.  # noqa: E501


        :return: The boot_cdrom of this ServerProperties.  # noqa: E501
        :rtype: ResourceReference
        """
        return self._boot_cdrom

    @boot_cdrom.setter
    def boot_cdrom(self, boot_cdrom):
        """Sets the boot_cdrom of this ServerProperties.


        :param boot_cdrom: The boot_cdrom of this ServerProperties.  # noqa: E501
        :type boot_cdrom: ResourceReference
        """

        self._boot_cdrom = boot_cdrom

    @property
    def boot_volume(self):
        """Gets the boot_volume of this ServerProperties.  # noqa: E501


        :return: The boot_volume of this ServerProperties.  # noqa: E501
        :rtype: ResourceReference
        """
        return self._boot_volume

    @boot_volume.setter
    def boot_volume(self, boot_volume):
        """Sets the boot_volume of this ServerProperties.


        :param boot_volume: The boot_volume of this ServerProperties.  # noqa: E501
        :type boot_volume: ResourceReference
        """

        self._boot_volume = boot_volume

    @property
    def cpu_family(self):
        """Gets the cpu_family of this ServerProperties.  # noqa: E501

        CPU architecture on which server gets provisioned; not all CPU architectures are available in all datacenter regions; available CPU architectures can be retrieved from the datacenter resource.  # noqa: E501

        :return: The cpu_family of this ServerProperties.  # noqa: E501
        :rtype: str
        """
        return self._cpu_family

    @cpu_family.setter
    def cpu_family(self, cpu_family):
        """Sets the cpu_family of this ServerProperties.

        CPU architecture on which server gets provisioned; not all CPU architectures are available in all datacenter regions; available CPU architectures can be retrieved from the datacenter resource.  # noqa: E501

        :param cpu_family: The cpu_family of this ServerProperties.  # noqa: E501
        :type cpu_family: str
        """

        self._cpu_family = cpu_family

    @property
    def type(self):
        """Gets the type of this ServerProperties.  # noqa: E501

        server usages: ENTERPRISE or CUBE  # noqa: E501

        :return: The type of this ServerProperties.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this ServerProperties.

        server usages: ENTERPRISE or CUBE  # noqa: E501

        :param type: The type of this ServerProperties.  # noqa: E501
        :type type: str
        """

        self._type = type
    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.openapi_types):
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

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, ServerProperties):
            return False

        return self.to_dict() == other.to_dict()

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        if not isinstance(other, ServerProperties):
            return True

        return self.to_dict() != other.to_dict()
