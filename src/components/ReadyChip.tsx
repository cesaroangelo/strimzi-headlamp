import React from 'react';
import { Chip } from '@mui/material';
import { useTheme } from '@mui/material/styles';
import { readyChipProps } from '../utils/readyChip';

export interface ReadyChipProps {
  /** Status of the `Ready` condition: `'True'`, `'False'`, `'Unknown'`, or absent. */
  status: string | undefined | null;
}

/**
 * The chip every Strimzi list uses for the `Ready` condition.
 *
 * Each list used to inline the same Chip markup and its own status-to-label
 * mapping, which had already drifted: the Connect lists went through
 * `readyChipProps` and so rendered the literal `'Unknown'` status as the
 * neutral chip, while the Kafka, Topic and User lists compared against `null`
 * only and showed it as "Not Ready". Sharing one component keeps the mapping
 * and the styling in one place.
 */
export function ReadyChip({ status }: ReadyChipProps) {
  const theme = useTheme();
  const { label, color } = readyChipProps(status);
  return (
    <Chip
      label={label}
      variant={theme.palette.mode === 'dark' ? 'outlined' : 'filled'}
      size="medium"
      color={color}
      sx={{ borderRadius: '4px' }}
    />
  );
}
