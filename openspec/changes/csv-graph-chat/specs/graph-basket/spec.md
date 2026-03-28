## ADDED Requirements

### Requirement: Save graph to basket
The system SHALL allow users to save the current graph configuration to a basket for later download.

#### Scenario: Save graph with default name
- **WHEN** user clicks "바구니에 담기" button
- **THEN** system SHALL save the current graph configuration with auto-generated name based on content
- **AND** display a toast success message "바구니에 담겼어요! 🛒"
- **AND** update the basket count

#### Scenario: Save fails
- **WHEN** user clicks "바구니에 담기" but save operation fails
- **THEN** system SHALL display a toast error "저장에 실패했어요. 다시 시도해주세요"
- **AND** not update the basket

### Requirement: View basket contents
The system SHALL display a sidebar showing all saved graphs in the basket.

#### Scenario: Display basket list
- **WHEN** user has saved graphs in the basket
- **THEN** system SHALL show a sidebar with:
- **AND** each graph as a card with name and timestamp
- **AND** preview button (eye icon)
- **AND** delete button (trash icon)

#### Scenario: Empty basket
- **WHEN** basket is empty
- **THEN** system SHALL display "바구니가 비어있어요"
- **AND** hide the download all button

### Requirement: Preview graph from basket
The system SHALL allow users to preview a saved graph in the main graph area.

#### Scenario: Preview graph
- **WHEN** user clicks preview button on a basket item
- **THEN** system SHALL load that graph configuration into the main chart area
- **AND** display it using Chart.js

### Requirement: Delete graph from basket
The system SHALL allow users to delete individual graphs from the basket.

#### Scenario: Delete single graph
- **WHEN** user clicks delete button on a basket item
- **THEN** system SHALL remove that graph from the basket
- **AND** update the basket count
- **AND** update the sidebar list

### Requirement: Download all graphs as HTML
The system SHALL allow users to download all basket graphs as a single HTML file or ZIP.

#### Scenario: Download all graphs
- **WHEN** user clicks "모두 다운로드" button
- **THEN** system SHALL generate an HTML file containing:
- **AND** all saved graphs rendered with Chart.js
- **AND** the original CSV data embedded or linked
- **AND** trigger browser download

#### Scenario: Single graph HTML download
- **WHEN** user wants to download a single graph
- **THEN** system SHALL generate HTML for just that graph
- **AND** trigger browser download

### Requirement: Basket data persistence
The system SHALL persist basket data server-side.

#### Scenario: Data persistence
- **WHEN** user saves a graph to basket
- **THEN** system SHALL store in database:
- **AND** graph configuration (JSON)
- **AND** associated CSV reference or data
- **AND** creation timestamp

#### Scenario: Session-less operation
- **WHEN** user has saved graphs in basket
- **AND** user reloads the page
- **THEN** basket SHALL remain populated (data persists on server)
