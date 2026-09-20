import React from 'react';
import { Button } from '@mui/material';
import {
  ResourceListView,
  type ColumnType,
  type ResourceTableColumn,
} from '@kinvolk/headlamp-plugin/lib/components/common';
import { Kafka } from '../resources/kafka';
import { KafkaTopologyModal } from './KafkaTopologyModal';
import type { KafkaInterface } from '../resources/kafka';
import { useStrimziApiVersions } from '../hooks/useStrimziApiVersions';
import { StrimziNotInstalledMessage } from './StrimziNotInstalledMessage';
import { ReadyChip } from './ReadyChip';
import { readyChipProps } from '../utils/readyChip';

export function KafkaList() {
  const { ready, installed } = useStrimziApiVersions();

  // All hooks must be called before any early return (Rules of Hooks).
  // `installed` flips from true to false once the API probe resolves, so
  // returning early above these would change the hook count between renders.
  const [selectedKafka, setSelectedKafka] = React.useState<KafkaInterface | null>(null);
  const [isTopologyModalOpen, setIsTopologyModalOpen] = React.useState(false);

  const columns: (ColumnType | ResourceTableColumn<Kafka>)[] = [
    'name',
    'namespace',
    {
      id: 'mode',
      label: 'Mode',
      getValue: (item: Kafka) => item.clusterMode,
    },
    {
      id: 'version',
      label: 'Version',
      getValue: (item: Kafka) => item.kafkaVersion,
    },
    {
      id: 'replicas',
      label: 'Replicas',
      getValue: (item: Kafka) => item.replicasDisplay,
    },
    {
      id: 'status',
      label: 'Status',
      getValue: (item: Kafka) => readyChipProps(item.readyStatus).label,
      render: (item: Kafka) => <ReadyChip status={item.readyStatus} />,
    },
    {
      id: 'topology',
      label: 'Topology',
      getValue: () => '',
      render: (item: Kafka) => (
        <Button
          size="small"
          variant="outlined"
          onClick={() => {
            setSelectedKafka(item.jsonData);
            setIsTopologyModalOpen(true);
          }}
        >
          View
        </Button>
      ),
    },
    'age',
  ];

  if (ready && !installed) return <StrimziNotInstalledMessage />;

  return (
    <>
      <ResourceListView
        title="Kafka Clusters"
        resourceClass={Kafka}
        columns={columns}
      />
      <KafkaTopologyModal
        kafka={selectedKafka}
        open={isTopologyModalOpen}
        onClose={() => {
          setIsTopologyModalOpen(false);
          setSelectedKafka(null);
        }}
      />
    </>
  );
}
