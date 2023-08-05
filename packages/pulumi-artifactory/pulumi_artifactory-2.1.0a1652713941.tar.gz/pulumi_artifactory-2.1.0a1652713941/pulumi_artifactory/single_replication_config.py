# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities

__all__ = ['SingleReplicationConfigArgs', 'SingleReplicationConfig']

@pulumi.input_type
class SingleReplicationConfigArgs:
    def __init__(__self__, *,
                 cron_exp: pulumi.Input[str],
                 repo_key: pulumi.Input[str],
                 enable_event_replication: Optional[pulumi.Input[bool]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 path_prefix: Optional[pulumi.Input[str]] = None,
                 proxy: Optional[pulumi.Input[str]] = None,
                 socket_timeout_millis: Optional[pulumi.Input[int]] = None,
                 sync_deletes: Optional[pulumi.Input[bool]] = None,
                 sync_properties: Optional[pulumi.Input[bool]] = None,
                 sync_statistics: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a SingleReplicationConfig resource.
        :param pulumi.Input[str] proxy: Proxy key from Artifactory Proxies setting.
        """
        pulumi.set(__self__, "cron_exp", cron_exp)
        pulumi.set(__self__, "repo_key", repo_key)
        if enable_event_replication is not None:
            pulumi.set(__self__, "enable_event_replication", enable_event_replication)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if path_prefix is not None:
            pulumi.set(__self__, "path_prefix", path_prefix)
        if proxy is not None:
            pulumi.set(__self__, "proxy", proxy)
        if socket_timeout_millis is not None:
            pulumi.set(__self__, "socket_timeout_millis", socket_timeout_millis)
        if sync_deletes is not None:
            pulumi.set(__self__, "sync_deletes", sync_deletes)
        if sync_properties is not None:
            pulumi.set(__self__, "sync_properties", sync_properties)
        if sync_statistics is not None:
            pulumi.set(__self__, "sync_statistics", sync_statistics)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="cronExp")
    def cron_exp(self) -> pulumi.Input[str]:
        return pulumi.get(self, "cron_exp")

    @cron_exp.setter
    def cron_exp(self, value: pulumi.Input[str]):
        pulumi.set(self, "cron_exp", value)

    @property
    @pulumi.getter(name="repoKey")
    def repo_key(self) -> pulumi.Input[str]:
        return pulumi.get(self, "repo_key")

    @repo_key.setter
    def repo_key(self, value: pulumi.Input[str]):
        pulumi.set(self, "repo_key", value)

    @property
    @pulumi.getter(name="enableEventReplication")
    def enable_event_replication(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enable_event_replication")

    @enable_event_replication.setter
    def enable_event_replication(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_event_replication", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter(name="pathPrefix")
    def path_prefix(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "path_prefix")

    @path_prefix.setter
    def path_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path_prefix", value)

    @property
    @pulumi.getter
    def proxy(self) -> Optional[pulumi.Input[str]]:
        """
        Proxy key from Artifactory Proxies setting.
        """
        return pulumi.get(self, "proxy")

    @proxy.setter
    def proxy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy", value)

    @property
    @pulumi.getter(name="socketTimeoutMillis")
    def socket_timeout_millis(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "socket_timeout_millis")

    @socket_timeout_millis.setter
    def socket_timeout_millis(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "socket_timeout_millis", value)

    @property
    @pulumi.getter(name="syncDeletes")
    def sync_deletes(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "sync_deletes")

    @sync_deletes.setter
    def sync_deletes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sync_deletes", value)

    @property
    @pulumi.getter(name="syncProperties")
    def sync_properties(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "sync_properties")

    @sync_properties.setter
    def sync_properties(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sync_properties", value)

    @property
    @pulumi.getter(name="syncStatistics")
    def sync_statistics(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "sync_statistics")

    @sync_statistics.setter
    def sync_statistics(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sync_statistics", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


@pulumi.input_type
class _SingleReplicationConfigState:
    def __init__(__self__, *,
                 cron_exp: Optional[pulumi.Input[str]] = None,
                 enable_event_replication: Optional[pulumi.Input[bool]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 password: Optional[pulumi.Input[str]] = None,
                 path_prefix: Optional[pulumi.Input[str]] = None,
                 proxy: Optional[pulumi.Input[str]] = None,
                 repo_key: Optional[pulumi.Input[str]] = None,
                 socket_timeout_millis: Optional[pulumi.Input[int]] = None,
                 sync_deletes: Optional[pulumi.Input[bool]] = None,
                 sync_properties: Optional[pulumi.Input[bool]] = None,
                 sync_statistics: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering SingleReplicationConfig resources.
        :param pulumi.Input[str] password: Requires password encryption to be turned off `POST /api/system/decrypt`.
        :param pulumi.Input[str] proxy: Proxy key from Artifactory Proxies setting.
        """
        if cron_exp is not None:
            pulumi.set(__self__, "cron_exp", cron_exp)
        if enable_event_replication is not None:
            pulumi.set(__self__, "enable_event_replication", enable_event_replication)
        if enabled is not None:
            pulumi.set(__self__, "enabled", enabled)
        if password is not None:
            pulumi.set(__self__, "password", password)
        if path_prefix is not None:
            pulumi.set(__self__, "path_prefix", path_prefix)
        if proxy is not None:
            pulumi.set(__self__, "proxy", proxy)
        if repo_key is not None:
            pulumi.set(__self__, "repo_key", repo_key)
        if socket_timeout_millis is not None:
            pulumi.set(__self__, "socket_timeout_millis", socket_timeout_millis)
        if sync_deletes is not None:
            pulumi.set(__self__, "sync_deletes", sync_deletes)
        if sync_properties is not None:
            pulumi.set(__self__, "sync_properties", sync_properties)
        if sync_statistics is not None:
            pulumi.set(__self__, "sync_statistics", sync_statistics)
        if url is not None:
            pulumi.set(__self__, "url", url)
        if username is not None:
            pulumi.set(__self__, "username", username)

    @property
    @pulumi.getter(name="cronExp")
    def cron_exp(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "cron_exp")

    @cron_exp.setter
    def cron_exp(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cron_exp", value)

    @property
    @pulumi.getter(name="enableEventReplication")
    def enable_event_replication(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enable_event_replication")

    @enable_event_replication.setter
    def enable_event_replication(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_event_replication", value)

    @property
    @pulumi.getter
    def enabled(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "enabled")

    @enabled.setter
    def enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enabled", value)

    @property
    @pulumi.getter
    def password(self) -> Optional[pulumi.Input[str]]:
        """
        Requires password encryption to be turned off `POST /api/system/decrypt`.
        """
        return pulumi.get(self, "password")

    @password.setter
    def password(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "password", value)

    @property
    @pulumi.getter(name="pathPrefix")
    def path_prefix(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "path_prefix")

    @path_prefix.setter
    def path_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "path_prefix", value)

    @property
    @pulumi.getter
    def proxy(self) -> Optional[pulumi.Input[str]]:
        """
        Proxy key from Artifactory Proxies setting.
        """
        return pulumi.get(self, "proxy")

    @proxy.setter
    def proxy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "proxy", value)

    @property
    @pulumi.getter(name="repoKey")
    def repo_key(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "repo_key")

    @repo_key.setter
    def repo_key(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "repo_key", value)

    @property
    @pulumi.getter(name="socketTimeoutMillis")
    def socket_timeout_millis(self) -> Optional[pulumi.Input[int]]:
        return pulumi.get(self, "socket_timeout_millis")

    @socket_timeout_millis.setter
    def socket_timeout_millis(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "socket_timeout_millis", value)

    @property
    @pulumi.getter(name="syncDeletes")
    def sync_deletes(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "sync_deletes")

    @sync_deletes.setter
    def sync_deletes(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sync_deletes", value)

    @property
    @pulumi.getter(name="syncProperties")
    def sync_properties(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "sync_properties")

    @sync_properties.setter
    def sync_properties(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sync_properties", value)

    @property
    @pulumi.getter(name="syncStatistics")
    def sync_statistics(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "sync_statistics")

    @sync_statistics.setter
    def sync_statistics(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "sync_statistics", value)

    @property
    @pulumi.getter
    def url(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "url")

    @url.setter
    def url(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "url", value)

    @property
    @pulumi.getter
    def username(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "username")

    @username.setter
    def username(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "username", value)


class SingleReplicationConfig(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cron_exp: Optional[pulumi.Input[str]] = None,
                 enable_event_replication: Optional[pulumi.Input[bool]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 path_prefix: Optional[pulumi.Input[str]] = None,
                 proxy: Optional[pulumi.Input[str]] = None,
                 repo_key: Optional[pulumi.Input[str]] = None,
                 socket_timeout_millis: Optional[pulumi.Input[int]] = None,
                 sync_deletes: Optional[pulumi.Input[bool]] = None,
                 sync_properties: Optional[pulumi.Input[bool]] = None,
                 sync_statistics: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Artifactory single replication config resource. This can be used to create and manage a single Artifactory
        replication. Primarily used when pull replication is needed.

        **WARNING: This should not be used on a repository with `ReplicationConfig`. Using both together will cause
        unexpected behaviour and will almost certainly cause your replications to break.**

        ## Import

        Replication configs can be imported using their repo key, e.g.

        ```sh
         $ pulumi import artifactory:index/singleReplicationConfig:SingleReplicationConfig foo-rep repository-key
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] proxy: Proxy key from Artifactory Proxies setting.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: SingleReplicationConfigArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Artifactory single replication config resource. This can be used to create and manage a single Artifactory
        replication. Primarily used when pull replication is needed.

        **WARNING: This should not be used on a repository with `ReplicationConfig`. Using both together will cause
        unexpected behaviour and will almost certainly cause your replications to break.**

        ## Import

        Replication configs can be imported using their repo key, e.g.

        ```sh
         $ pulumi import artifactory:index/singleReplicationConfig:SingleReplicationConfig foo-rep repository-key
        ```

        :param str resource_name: The name of the resource.
        :param SingleReplicationConfigArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(SingleReplicationConfigArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cron_exp: Optional[pulumi.Input[str]] = None,
                 enable_event_replication: Optional[pulumi.Input[bool]] = None,
                 enabled: Optional[pulumi.Input[bool]] = None,
                 path_prefix: Optional[pulumi.Input[str]] = None,
                 proxy: Optional[pulumi.Input[str]] = None,
                 repo_key: Optional[pulumi.Input[str]] = None,
                 socket_timeout_millis: Optional[pulumi.Input[int]] = None,
                 sync_deletes: Optional[pulumi.Input[bool]] = None,
                 sync_properties: Optional[pulumi.Input[bool]] = None,
                 sync_statistics: Optional[pulumi.Input[bool]] = None,
                 url: Optional[pulumi.Input[str]] = None,
                 username: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = SingleReplicationConfigArgs.__new__(SingleReplicationConfigArgs)

            if cron_exp is None and not opts.urn:
                raise TypeError("Missing required property 'cron_exp'")
            __props__.__dict__["cron_exp"] = cron_exp
            __props__.__dict__["enable_event_replication"] = enable_event_replication
            __props__.__dict__["enabled"] = enabled
            __props__.__dict__["path_prefix"] = path_prefix
            __props__.__dict__["proxy"] = proxy
            if repo_key is None and not opts.urn:
                raise TypeError("Missing required property 'repo_key'")
            __props__.__dict__["repo_key"] = repo_key
            __props__.__dict__["socket_timeout_millis"] = socket_timeout_millis
            __props__.__dict__["sync_deletes"] = sync_deletes
            __props__.__dict__["sync_properties"] = sync_properties
            __props__.__dict__["sync_statistics"] = sync_statistics
            __props__.__dict__["url"] = url
            __props__.__dict__["username"] = username
            __props__.__dict__["password"] = None
        super(SingleReplicationConfig, __self__).__init__(
            'artifactory:index/singleReplicationConfig:SingleReplicationConfig',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cron_exp: Optional[pulumi.Input[str]] = None,
            enable_event_replication: Optional[pulumi.Input[bool]] = None,
            enabled: Optional[pulumi.Input[bool]] = None,
            password: Optional[pulumi.Input[str]] = None,
            path_prefix: Optional[pulumi.Input[str]] = None,
            proxy: Optional[pulumi.Input[str]] = None,
            repo_key: Optional[pulumi.Input[str]] = None,
            socket_timeout_millis: Optional[pulumi.Input[int]] = None,
            sync_deletes: Optional[pulumi.Input[bool]] = None,
            sync_properties: Optional[pulumi.Input[bool]] = None,
            sync_statistics: Optional[pulumi.Input[bool]] = None,
            url: Optional[pulumi.Input[str]] = None,
            username: Optional[pulumi.Input[str]] = None) -> 'SingleReplicationConfig':
        """
        Get an existing SingleReplicationConfig resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] password: Requires password encryption to be turned off `POST /api/system/decrypt`.
        :param pulumi.Input[str] proxy: Proxy key from Artifactory Proxies setting.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _SingleReplicationConfigState.__new__(_SingleReplicationConfigState)

        __props__.__dict__["cron_exp"] = cron_exp
        __props__.__dict__["enable_event_replication"] = enable_event_replication
        __props__.__dict__["enabled"] = enabled
        __props__.__dict__["password"] = password
        __props__.__dict__["path_prefix"] = path_prefix
        __props__.__dict__["proxy"] = proxy
        __props__.__dict__["repo_key"] = repo_key
        __props__.__dict__["socket_timeout_millis"] = socket_timeout_millis
        __props__.__dict__["sync_deletes"] = sync_deletes
        __props__.__dict__["sync_properties"] = sync_properties
        __props__.__dict__["sync_statistics"] = sync_statistics
        __props__.__dict__["url"] = url
        __props__.__dict__["username"] = username
        return SingleReplicationConfig(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cronExp")
    def cron_exp(self) -> pulumi.Output[str]:
        return pulumi.get(self, "cron_exp")

    @property
    @pulumi.getter(name="enableEventReplication")
    def enable_event_replication(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "enable_event_replication")

    @property
    @pulumi.getter
    def enabled(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "enabled")

    @property
    @pulumi.getter
    def password(self) -> pulumi.Output[str]:
        """
        Requires password encryption to be turned off `POST /api/system/decrypt`.
        """
        return pulumi.get(self, "password")

    @property
    @pulumi.getter(name="pathPrefix")
    def path_prefix(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "path_prefix")

    @property
    @pulumi.getter
    def proxy(self) -> pulumi.Output[Optional[str]]:
        """
        Proxy key from Artifactory Proxies setting.
        """
        return pulumi.get(self, "proxy")

    @property
    @pulumi.getter(name="repoKey")
    def repo_key(self) -> pulumi.Output[str]:
        return pulumi.get(self, "repo_key")

    @property
    @pulumi.getter(name="socketTimeoutMillis")
    def socket_timeout_millis(self) -> pulumi.Output[int]:
        return pulumi.get(self, "socket_timeout_millis")

    @property
    @pulumi.getter(name="syncDeletes")
    def sync_deletes(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "sync_deletes")

    @property
    @pulumi.getter(name="syncProperties")
    def sync_properties(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "sync_properties")

    @property
    @pulumi.getter(name="syncStatistics")
    def sync_statistics(self) -> pulumi.Output[bool]:
        return pulumi.get(self, "sync_statistics")

    @property
    @pulumi.getter
    def url(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "url")

    @property
    @pulumi.getter
    def username(self) -> pulumi.Output[Optional[str]]:
        return pulumi.get(self, "username")

