import React from 'react';
import { Box } from '@mui/material';
import {
  DateLabel,
  SectionHeader,
  SimpleTable,
} from '@kinvolk/headlamp-plugin/lib/components/common';
import { Meta, StoryObj } from '@storybook/react';
import type { KafkaConnectInterface } from '../resources/kafkaConnect';
import { ReadyChip } from './ReadyChip';
import { mockKafkaConnects } from '../storybookMocks/strimziMocks';

function connectReadyStatus(c: KafkaConnectInterface): string {
  const condition = c.status?.conditions?.find(x => x.type === 'Ready');
  return condition?.status ?? 'Unknown';
}

interface PureKafkaConnectListProps {
  items: KafkaConnectInterface[];
}

/**
 * Storybook-only presentation component for KafkaConnect list rows.
 * Does not call the Kubernetes API; mirrors the columns and chip styling
 * of the production `KafkaConnectList` component so reviewers can poke at
 * it without a cluster.
 */
export function PureKafkaConnectList({ items }: PureKafkaConnectListProps) {
  return (
    <Box>
      <SectionHeader title="Kafka Connect Clusters" />
      <SimpleTable
        columns={[
          { label: 'Name', getter: row => row.metadata.name },
          { label: 'Namespace', getter: row => row.metadata.namespace },
          { label: 'Version', getter: row => row.spec?.version ?? 'N/A' },
          { label: 'Replicas', getter: row => row.spec?.replicas ?? 0 },
          { label: 'Bootstrap servers', getter: row => row.spec?.bootstrapServers ?? '-' },
          { label: 'Plugins', getter: row => row.status?.connectorPlugins?.length ?? 0 },
          {
            label: 'Status',
            getter: (row: KafkaConnectInterface) => <ReadyChip status={connectReadyStatus(row)} />,
          },
          {
            label: 'Age',
            getter: row => <DateLabel date={row.metadata.creationTimestamp} format="mini" />,
          },
        ]}
        data={items}
        emptyMessage="No Kafka Connect clusters found"
      />
    </Box>
  );
}

const meta: Meta<typeof PureKafkaConnectList> = {
  title: 'strimzi/KafkaConnectList',
  component: PureKafkaConnectList,
};
export default meta;

type Story = StoryObj<typeof PureKafkaConnectList>;

export const Default: Story = {
  args: { items: mockKafkaConnects },
};

export const Empty: Story = {
  args: { items: [] },
};
