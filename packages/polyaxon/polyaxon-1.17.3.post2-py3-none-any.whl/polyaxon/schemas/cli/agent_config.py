#!/usr/bin/python
#
# Copyright 2018-2021 Polyaxon, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from typing import List

from marshmallow import EXCLUDE, ValidationError, fields, pre_load, validates_schema

from polyaxon.auxiliaries import (
    DefaultSchedulingSchema,
    PolyaxonCleanerSchema,
    PolyaxonInitContainerSchema,
    PolyaxonNotifierSchema,
    PolyaxonSidecarContainerSchema,
    V1DefaultScheduling,
)
from polyaxon.containers.contexts import CONTEXT_ARTIFACTS_ROOT
from polyaxon.env_vars.keys import (
    POLYAXON_KEYS_AGENT_ARTIFACTS_STORE,
    POLYAXON_KEYS_AGENT_CLEANER,
    POLYAXON_KEYS_AGENT_COMPRESSED_LOGS,
    POLYAXON_KEYS_AGENT_CONNECTIONS,
    POLYAXON_KEYS_AGENT_DEFAULT_IMAGE_PULL_SECRETS,
    POLYAXON_KEYS_AGENT_DEFAULT_SCHEDULING,
    POLYAXON_KEYS_AGENT_INIT,
    POLYAXON_KEYS_AGENT_IS_REPLICA,
    POLYAXON_KEYS_AGENT_NOTIFIER,
    POLYAXON_KEYS_AGENT_RUNS_SA,
    POLYAXON_KEYS_AGENT_SECRET_NAME,
    POLYAXON_KEYS_AGENT_SIDECAR,
    POLYAXON_KEYS_AGENT_SPAWNER_REFRESH_INTERVAL,
    POLYAXON_KEYS_AGENT_USE_PROXY_ENV_VARS_IN_OPS,
    POLYAXON_KEYS_K8S_APP_SECRET_NAME,
    POLYAXON_KEYS_K8S_NAMESPACE,
)
from polyaxon.exceptions import PolyaxonSchemaError
from polyaxon.parser import parser
from polyaxon.schemas.base import BaseConfig, BaseSchema
from polyaxon.schemas.types import ConnectionTypeSchema, V1K8sResourceType
from polyaxon.utils.signal_decorators import check_partial


def validate_agent_config(artifacts_store, connections):
    if not artifacts_store:
        raise ValidationError(
            "A connection definition is required to set a default artifacts store."
        )

    connections = connections or []

    connection_names = set()

    connection_names.add(artifacts_store.name)

    for c in connections:
        if c.name in connection_names:
            raise ValidationError(
                "A connection with name `{}` must be unique.".format(c.name)
            )
        connection_names.add(c.name)


class AgentSchema(BaseSchema):
    namespace = fields.Str(allow_none=True, data_key=POLYAXON_KEYS_K8S_NAMESPACE)
    is_replica = fields.Bool(allow_none=True, data_key=POLYAXON_KEYS_AGENT_IS_REPLICA)
    compressed_logs = fields.Bool(
        allow_none=True, data_key=POLYAXON_KEYS_AGENT_COMPRESSED_LOGS
    )
    sidecar = fields.Nested(
        PolyaxonSidecarContainerSchema,
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_SIDECAR,
    )
    init = fields.Nested(
        PolyaxonInitContainerSchema, allow_none=True, data_key=POLYAXON_KEYS_AGENT_INIT
    )
    notifier = fields.Nested(
        PolyaxonNotifierSchema, allow_none=True, data_key=POLYAXON_KEYS_AGENT_NOTIFIER
    )
    cleaner = fields.Nested(
        PolyaxonCleanerSchema, allow_none=True, data_key=POLYAXON_KEYS_AGENT_CLEANER
    )
    use_proxy_env_vars_use_in_ops = fields.Bool(
        allow_none=True, data_key=POLYAXON_KEYS_AGENT_USE_PROXY_ENV_VARS_IN_OPS
    )
    default_scheduling = fields.Nested(
        DefaultSchedulingSchema,
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_DEFAULT_SCHEDULING,
    )
    default_image_pull_secrets = fields.List(
        fields.Str(),
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_DEFAULT_IMAGE_PULL_SECRETS,
    )
    artifacts_store = fields.Nested(
        ConnectionTypeSchema,
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_ARTIFACTS_STORE,
    )
    connections = fields.List(
        fields.Nested(ConnectionTypeSchema),
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_CONNECTIONS,
    )
    app_secret_name = fields.Str(
        allow_none=True,
        data_key=POLYAXON_KEYS_K8S_APP_SECRET_NAME,
    )
    agent_secret_name = fields.Str(
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_SECRET_NAME,
    )
    runs_sa = fields.Str(
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_RUNS_SA,
    )
    # This refresh logic will mitigate several issues with AKS's numerous networking problems
    spawner_refresh_interval = fields.Integer(
        allow_none=True,
        data_key=POLYAXON_KEYS_AGENT_SPAWNER_REFRESH_INTERVAL,
    )

    @staticmethod
    def schema_config():
        return AgentConfig

    @validates_schema
    @check_partial
    def validate_connection(self, data, **kwargs):
        validate_agent_config(data.get("artifacts_store"), data.get("connections"))

    @pre_load
    def pre_validate(self, data, **kwargs):
        connections = data.get(POLYAXON_KEYS_AGENT_CONNECTIONS)
        try:
            connections = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_CONNECTIONS,
                value=connections,
                is_list=True,
                is_optional=True,
            )
        except PolyaxonSchemaError as e:
            raise ValidationError("Received an invalid connections") from e
        if connections:
            data[POLYAXON_KEYS_AGENT_CONNECTIONS] = connections

        artifacts_store = data.get(POLYAXON_KEYS_AGENT_ARTIFACTS_STORE)
        try:
            artifacts_store = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_ARTIFACTS_STORE,
                value=artifacts_store,
                is_optional=True,
            )
        except PolyaxonSchemaError as e:
            raise ValidationError(
                "Received an invalid artifacts store `{}`".format(artifacts_store)
            ) from e
        if artifacts_store:
            data[POLYAXON_KEYS_AGENT_ARTIFACTS_STORE] = artifacts_store

        sidecar = data.get(POLYAXON_KEYS_AGENT_SIDECAR)
        try:
            sidecar = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_SIDECAR, value=sidecar, is_optional=True
            )
        except PolyaxonSchemaError as e:
            raise ValidationError(
                "Received an invalid sidecar `{}`".format(sidecar)
            ) from e
        if sidecar:
            data[POLYAXON_KEYS_AGENT_SIDECAR] = sidecar

        init = data.get(POLYAXON_KEYS_AGENT_INIT)
        try:
            init = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_INIT, value=init, is_optional=True
            )
        except PolyaxonSchemaError as e:
            raise ValidationError("Received an invalid init `{}`".format(init)) from e
        if init:
            data[POLYAXON_KEYS_AGENT_INIT] = init

        cleaner = data.get(POLYAXON_KEYS_AGENT_CLEANER)
        try:
            cleaner = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_CLEANER, value=cleaner, is_optional=True
            )
        except PolyaxonSchemaError as e:
            raise ValidationError(
                "Received an invalid cleaner `{}`".format(cleaner)
            ) from e
        if cleaner:
            data[POLYAXON_KEYS_AGENT_CLEANER] = cleaner

        notifier = data.get(POLYAXON_KEYS_AGENT_NOTIFIER)
        try:
            notifier = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_NOTIFIER, value=notifier, is_optional=True
            )
        except PolyaxonSchemaError as e:
            raise ValidationError(
                "Received an invalid notifier `{}`".format(notifier)
            ) from e
        if notifier:
            data[POLYAXON_KEYS_AGENT_NOTIFIER] = notifier

        default_scheduling = data.get(POLYAXON_KEYS_AGENT_DEFAULT_SCHEDULING)
        try:
            default_scheduling = parser.get_dict(
                key=POLYAXON_KEYS_AGENT_DEFAULT_SCHEDULING,
                value=default_scheduling,
                is_optional=True,
            )
        except PolyaxonSchemaError as e:
            raise ValidationError(
                "Received an invalid default_scheduling `{}`".format(default_scheduling)
            ) from e
        if default_scheduling:
            data[POLYAXON_KEYS_AGENT_DEFAULT_SCHEDULING] = default_scheduling

        default_image_pull_secrets = data.get(
            POLYAXON_KEYS_AGENT_DEFAULT_IMAGE_PULL_SECRETS
        )
        try:
            default_image_pull_secrets = parser.get_string(
                key=POLYAXON_KEYS_AGENT_DEFAULT_IMAGE_PULL_SECRETS,
                value=default_image_pull_secrets,
                is_optional=True,
                is_list=True,
            )
        except PolyaxonSchemaError as e:
            raise ValidationError(
                "Received an invalid default_image_pull_secrets `{}`".format(
                    default_image_pull_secrets
                )
            ) from e
        if default_image_pull_secrets:
            data[
                POLYAXON_KEYS_AGENT_DEFAULT_IMAGE_PULL_SECRETS
            ] = default_image_pull_secrets

        return data


class AgentConfig(BaseConfig):
    SCHEMA = AgentSchema
    IDENTIFIER = "agent"
    UNKNOWN_BEHAVIOUR = EXCLUDE
    REDUCED_ATTRIBUTES = [
        POLYAXON_KEYS_AGENT_SIDECAR,
        POLYAXON_KEYS_AGENT_INIT,
        POLYAXON_KEYS_AGENT_NOTIFIER,
        POLYAXON_KEYS_AGENT_CLEANER,
        POLYAXON_KEYS_AGENT_IS_REPLICA,
        POLYAXON_KEYS_AGENT_COMPRESSED_LOGS,
        POLYAXON_KEYS_AGENT_ARTIFACTS_STORE,
        POLYAXON_KEYS_AGENT_CONNECTIONS,
        POLYAXON_KEYS_K8S_APP_SECRET_NAME,
        POLYAXON_KEYS_AGENT_SECRET_NAME,
        POLYAXON_KEYS_AGENT_RUNS_SA,
        POLYAXON_KEYS_AGENT_SPAWNER_REFRESH_INTERVAL,
        POLYAXON_KEYS_AGENT_USE_PROXY_ENV_VARS_IN_OPS,
        POLYAXON_KEYS_AGENT_DEFAULT_SCHEDULING,
        POLYAXON_KEYS_AGENT_DEFAULT_IMAGE_PULL_SECRETS,
    ]

    def __init__(
        self,
        namespace=None,
        is_replica=None,
        compressed_logs=None,
        sidecar=None,
        init=None,
        notifier=None,
        cleaner=None,
        artifacts_store=None,
        connections=None,
        app_secret_name=None,
        agent_secret_name=None,
        runs_sa=None,
        spawner_refresh_interval=None,
        default_scheduling=None,
        use_proxy_env_vars_use_in_ops=None,
        default_image_pull_secrets=None,
        **kwargs
    ):
        self.namespace = namespace
        self.is_replica = is_replica
        self.compressed_logs = compressed_logs
        self.sidecar = sidecar
        self.init = init
        self.notifier = notifier
        self.cleaner = cleaner
        self.artifacts_store = artifacts_store
        self.connections = connections or []
        self.app_secret_name = app_secret_name
        self.agent_secret_name = agent_secret_name
        self.runs_sa = runs_sa
        self.spawner_refresh_interval = spawner_refresh_interval
        self.default_image_pull_secrets = default_image_pull_secrets
        self.use_proxy_env_vars_use_in_ops = use_proxy_env_vars_use_in_ops
        self.default_scheduling = default_scheduling
        if not self.default_scheduling and self.default_image_pull_secrets:
            self.default_scheduling = V1DefaultScheduling()
        if self.default_scheduling and not self.default_scheduling.image_pull_secrets:
            self.default_scheduling.image_pull_secrets = self.default_image_pull_secrets
        self._all_connections = []
        self.set_all_connections()
        self._secrets = None
        self._config_maps = None
        self._connections_by_names = {}

    def get_spawner_refresh_interval(self):
        return self.spawner_refresh_interval or 60 * 5

    def set_all_connections(self):
        self._all_connections = self.connections[:]
        if self.artifacts_store:
            self._all_connections.append(self.artifacts_store)
            validate_agent_config(self.artifacts_store, self.connections)

    @property
    def all_connections(self):
        return self._all_connections

    @property
    def secrets(self) -> List[V1K8sResourceType]:
        if self._secrets or not self._all_connections:
            return self._secrets
        secret_names = set()
        secrets = []
        for c in self._all_connections:
            if c.secret and c.secret.name not in secret_names:
                secret_names.add(c.secret.name)
                secrets.append(c.get_secret())
        self._secrets = secrets
        return self._secrets

    @property
    def config_maps(self) -> List[V1K8sResourceType]:
        if self._config_maps or not self._all_connections:
            return self._config_maps
        config_map_names = set()
        config_maps = []
        for c in self._all_connections:
            if c.config_map and c.config_map.name not in config_map_names:
                config_map_names.add(c.config_map.name)
                config_maps.append(c.get_config_map())
        self._config_maps = config_maps
        return self._config_maps

    @property
    def connections_by_names(self):
        if self._connections_by_names or not self._all_connections:
            return self._connections_by_names

        self._connections_by_names = {c.name: c for c in self._all_connections}
        return self._connections_by_names

    @property
    def artifacts_root(self):
        artifacts_root = CONTEXT_ARTIFACTS_ROOT
        if not self.artifacts_store:
            return artifacts_root

        if self.artifacts_store.is_mount:
            return self.artifacts_store.store_path

        return artifacts_root
