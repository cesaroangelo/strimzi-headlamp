# Changelog

All notable changes to this project will be documented in this file.

## [0.5.0] - 2026-09-20

### Added
- Kafka Connect: list and detail views for `KafkaConnect` clusters, including
  the connector plugins discovered by the operator and the Connect REST URL
- Kafka Connectors: list and detail views for `KafkaConnector`, with pause,
  resume and start applied as a JSON merge-patch on `spec.state` so the action
  is safe on GitOps-managed resources; credential-like config keys are masked
  behind an explicit reveal step
- Detail pages for Kafka, KafkaTopic, KafkaUser, KafkaConnect and KafkaConnector
- Resource Map integration, with edges from topics, users and connectors to the
  Kafka cluster named in their `strimzi.io/cluster` label
- Kind icons for all five Strimzi resource types
- Support for Strimzi 1.x: the resource classes declare both `v1` and `v1beta2`,
  and a runtime probe of `/apis` picks the version the cluster actually serves
- A friendly empty state when the Strimzi CRDs are not installed, and an error
  boundary so a plugin error can never take down Headlamp's root React tree
- Storybook with MSW mocks, and sample manifests under `test-files/`
- `react-hooks` lint rules, enabled as errors

### Changed
- Lists are built on Headlamp's `ResourceListView` and the resources on
  `KubeObject` classes, which cut the list components by about two thirds
- The `Ready` condition renders through one shared `ReadyChip` everywhere,
  and the status columns sort and search on the label they display
- headlamp-plugin 0.13.0 to 0.14.0

### Fixed
- Crash on the Kafka Topics and Users pages when the Kafka cluster list was
  still loading
- Crash on the Kafka Clusters and Kafka Connectors pages on a cluster without
  Strimzi installed, caused by hooks called after an early return
- Topology edit buttons pointing at `v1beta2` URLs on Strimzi 1.x clusters
- A `Ready` condition reported as `Unknown` shown as "Not Ready" on the Topics
  and Users lists
- Toast leaking its fade-out timer when unmounted mid-animation
- Wasted re-renders on the Topics and Users lists from an unmemoised fallback

### Removed
- The `SearchFilter` component, superseded by `ResourceListView`'s own search
- The `main` field from `package.json`, which Headlamp does not use

## [0.3.9] - 2026-03-07

### Added
- Edit buttons on topology nodes (Kafka, KafkaNodePool, StrimziPodSet)
- Monaco editor for viewing/editing resources as JSON
- Support for all topology modes: KRaft with NodePools, KRaft legacy, ZooKeeper

### Fixed
- Topology going blank after closing editor (event bubbling fix)
- Memory leak on setTimeout cleanup
- Unsafe non-null assertion in node pool lookup

## [0.3.8] - 2026-02-24

### Changed
- Automated Artifact Hub metadata update on release (version, date, archive URL, checksum)

## [0.3.7] - 2026-02-16

### Added
- Artifact Hub badge in README
- Demo video in README

### Changed
- Cleaned up repository documentation

## [0.3.1 - 0.3.6] - 2026-02-16

### Fixed
- Release workflow fixes (package name, npm publish configuration)

## [0.3.0] - 2025-01-30

### Added
- Namespace filter dropdown on all resource lists
- Cluster selection dropdown in Create Topic and Create User dialogs
- Minimal RBAC deployment configuration for production environments

### Changed
- Improved sidebar icon (streamline-ultimate:share)
- Updated deployment documentation

## [0.2.8] - 2025-01-28

### Fixed
- Namespace filter functionality across all components

## [0.2.7] - 2025-01-28

### Changed
- Replaced HTML buttons with Material-UI Button components for consistency

## [0.2.6] - 2025-01-28

### Changed
- Updated headlamp-plugin SDK to stable 0.13.0
- Fixed cluster link styling

## [0.2.5] - 2025-01-28

### Fixed
- ReactFlow attribution badge now theme-aware

## [0.2.4] - 2025-01-28

### Fixed
- Icon colors and badge text contrast in dark mode
- Replaced hardcoded colors with theme-aware palette

## [0.2.3] - 2025-01-28

### Fixed
- Kafka Replicas column display in cluster list
- Toast notifications now consistent across all components

## [0.2.2] - 2025-01-28

### Fixed
- Topology visualization in light mode
- Grid dots visibility in light mode
- Pod blocks visibility in light mode

## [0.2.1] - 2025-01-28

### Added
- Progressive background opacity for nested topology blocks
- Replica counts and ready status in topology view

### Fixed
- KafkaNodePool positioning for consistent layout
- ESLint warnings (removed unused variables)

## [0.2.0] - 2025-01-27

### Added
- Headlamp theme system integration with Kafka topology visualization
- Dynamic pod sizing in topology visualization
- Namespace wrapper in topology view
- Custom ReactFlow controls

### Fixed
- Topology centered at 1:1 scale without auto-zoom
- Improved ReactFlow controls and attribution visibility
- Removed MiniMap (incompatible with group nodes)

### Changed
- Refactored topology view to use modal instead of dedicated page
- Updated topology labels to show type and name on two lines

## [0.1.0] - 2025-01-27

Initial release.

### Features
- Kafka cluster visualization (KRaft/ZooKeeper detection)
- KafkaTopic CRUD operations
- KafkaUser management (SCRAM-SHA-512, TLS, ACLs)
- Search and filtering
- Secure credential display with warnings
- Topology visualization
