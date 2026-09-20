import React from 'react';
import { ConditionsSection, DetailsGrid } from '@kinvolk/headlamp-plugin/lib/components/common';
import { useParams } from 'react-router-dom';
import { KafkaUser } from '../../resources/kafkaUser';
import { ReadyChip } from '../ReadyChip';

export function KafkaUserDetail(props: { namespace?: string; name?: string }) {
  const params = useParams<{ namespace: string; name: string }>();
  const { namespace = params.namespace, name = params.name } = props;

  return (
    <DetailsGrid
      resourceType={KafkaUser}
      name={name}
      namespace={namespace}
      withEvents
      extraInfo={item =>
        item
          ? [
              { name: 'Authentication', value: item.authenticationType },
              { name: 'Authorization', value: item.authorizationType },
              { name: 'Status', value: <ReadyChip status={item.readyStatus} /> },
            ]
          : []
      }
      extraSections={item =>
        item
          ? [
              {
                id: 'conditions',
                section: <ConditionsSection resource={item?.jsonData} />,
              },
            ]
          : []
      }
    />
  );
}
