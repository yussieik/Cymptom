#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 10:41:08 2022

@author: Yossi Eikelman
"""

from dataclasses import dataclass, field
from utils import get_logger, extract_fields

logger = get_logger('INSTANCE')


@dataclass(repr=False)
class InstanceInfo:
    """Extractor for pulling instances from AWS EC2."""

    instance_name: str
    in_fields: dict

    def __repr__(self):
        kws = [f"{key} = {value}\n" for key, value in self.fields.items()]
        return "Instance: {}\n{}({})".format(self.instance_name, type(self).__name__, "".join(kws))


@dataclass(repr=False)
class Ids(InstanceInfo):
    """Instance Ids."""

    info_name: str = field(default='ids', metadata={
        'ids': 'ImageId, InstanceId'})
    keys = ['Id']

    def __post_init__(self):
        """Input relevant fields to Ids's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class OSPlatform(InstanceInfo):
    """Instance Operational system and Platform."""

    info_name: str = field(default='os', metadata={
        'os/platform': 'Block device mappings'})
    keys = ['Device']

    def __post_init__(self):
        """Input relevant fields to OSPlatform's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class NetworkSets(InstanceInfo):
    """Instance Network settings."""

    info_name: str = field(default='network settings', metadata={
        'os/platform': 'IPs, DNS, subnet, interfaces'})
    keys = ['Ebs', 'Network', 'Ip', 'Dns', 'Subnet']

    def __post_init__(self):
        """Input relevant fields to NetworkSets's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class Status(InstanceInfo):
    """Instance Status (stopped/running)."""

    info_name: str = field(default='status', metadata={
        'status': 'stopped/running, code'})
    keys = ['Monitoring_State', 'State_Name', 'Status']

    def __post_init__(self):
        """Input relevant fields to Status fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class Description(InstanceInfo):
    """Instance Description."""

    info_name: str = field(default='status', metadata={
        'status': 'stopped/running, code'})
    keys = ['Monitoring_State', 'State_Name']

    def __post_init__(self):
        """Input relevant fields to Description's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class LaunchTime(InstanceInfo):
    """Instance Launch Time."""

    info_name: str = field(default='launch time', metadata={
        'launch time': 'LaunchTime'})
    keys = ['LaunchTime']

    def __post_init__(self):
        """Input relevant fields to LaunchTime's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class Tags(InstanceInfo):
    """Instance Tags."""

    info_name: str = field(default='tags', metadata={'tags': 'LaunchTime'})
    keys = ['Tags']

    def __post_init__(self):
        """Input relevant fields to Tags's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class Specs(InstanceInfo):
    """Instance Specifications."""

    info_name: str = field(default='specs', metadata={
        'specs': 'cpu, ram, instance type'})
    keys = ['Cpu', 'Ram', 'InstanceType']

    def __post_init__(self):
        """Input relevant fields to Specs's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class SecurityGroups(InstanceInfo):
    """Instance Security Groups."""

    info_name: str = field(default='security_groups', metadata={
        'security groups': 'group name, group id'})
    keys = ['SecurityGroups']

    def __post_init__(self):
        """Input relevant fields to SecurityGroup's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass(repr=False)
class Tokens(InstanceInfo):
    """Instance Tokens."""
    info_name: str = field(default='tokens', metadata={
        'tokens': 'client token'})
    keys = ['Tokens']

    def __post_init__(self):
        """Input relevant fields to Token's fields."""
        self.fields = extract_fields(self.in_fields, self.keys)


@dataclass
class Instance:
    """Instance class with relevant Informational sub-Instances."""

    instance_name: str
    in_fields: dict

    def __post_init__(self):
        """Populates Instance's Informational sub-Instances ."""
        self.ids = Ids(self.instance_name, self.in_fields)
        self.os_platform = OSPlatform(self.instance_name, self.in_fields)
        self.network_sets = NetworkSets(self.instance_name, self.in_fields)
        self.status = Status(self.instance_name, self.in_fields)
        self.description = Description(self.instance_name, self.in_fields)
        self.launch_time = LaunchTime(self.instance_name, self.in_fields)
        self.tags = Tags(self.instance_name, self.in_fields)
        self.specs = Specs(self.instance_name, self.in_fields)
        self.security_groups = SecurityGroups(
            self.instance_name, self.in_fields)
        self.tokens = Tokens(self.instance_name, self.in_fields)
        logger.info(
            f"CREATED: Instance {self.instance_name} with {len(self.in_fields)} fields.")
