import React from 'react';
import {
  ResourceListView,
  type ColumnType,
  type ResourceTableColumn,
} from '@kinvolk/headlamp-plugin/lib/components/common';
import { KafkaConnect } from '../resources/kafkaConnect';
import { readyChipProps } from '../utils/readyChip';
import { ReadyChip } from './ReadyChip';
import { useStrimziApiVersions } from '../hooks/useStrimziApiVersions';
import { StrimziNotInstalledMessage } from './StrimziNotInstalledMessage';

/**
 * List view for Strimzi `KafkaConnect` resources (Kafka Connect clusters).
 *
 * Read-only at the list level: cluster creation involves many fields
 * (image, version, config, TLS, auth, …) that are best authored as YAML.
 * The detail view exposes the full spec, conditions, and discovered
 * connector plugins.
 */
export function KafkaConnectList() {
  const { ready, installed } = useStrimziApiVersions();

  if (ready && !installed) return <StrimziNotInstalledMessage />;

  const columns: (ColumnType | ResourceTableColumn<KafkaConnect>)[] = [
    'name',
    'namespace',
    {
      id: 'version',
      label: 'Version',
      getValue: (item: KafkaConnect) => item.connectVersion,
    },
    {
      id: 'replicas',
      label: 'Replicas',
      getValue: (item: KafkaConnect) => item.replicas,
    },
    {
      id: 'bootstrap',
      label: 'Bootstrap servers',
      getValue: (item: KafkaConnect) => item.bootstrapServers,
    },
    {
      id: 'plugins',
      label: 'Plugins',
      getValue: (item: KafkaConnect) => item.connectorPlugins.length,
    },
    {
      id: 'status',
      label: 'Status',
      getValue: (item: KafkaConnect) => readyChipProps(item.readyStatus).label,
      render: (item: KafkaConnect) => <ReadyChip status={item.readyStatus} />,
    },
    'age',
  ];

  return (
    <ResourceListView title="Kafka Connect Clusters" resourceClass={KafkaConnect} columns={columns} />
  );
}
