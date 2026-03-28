## ADDED Requirements

### Requirement: CSV file upload
The system SHALL allow users to upload CSV files via the frontend interface. The file size MUST NOT exceed 10MB.

#### Scenario: Successful file upload
- **WHEN** user selects a CSV file and clicks upload
- **THEN** system validates the file is under 10MB and is a valid CSV
- **AND** system returns the CSV data and detected columns

#### Scenario: File size exceeded
- **WHEN** user selects a CSV file larger than 10MB
- **THEN** system SHALL display a toast error message "파일이 너무 커요 (10MB 이하로 올려주세요)"
- **AND** upload is rejected

#### Scenario: Invalid file format
- **WHEN** user selects a non-CSV file
- **THEN** system SHALL display a toast error message "CSV 파일만 업로드 가능합니다"
- **AND** upload is rejected

### Requirement: Automatic header detection
The system SHALL automatically detect whether the CSV has meaningful headers or no headers (first row is data).

#### Scenario: CSV with meaningful headers
- **WHEN** CSV contains headers like "date", "sales", "region"
- **THEN** system SHALL use those headers as column names

#### Scenario: CSV with meaningless headers
- **WHEN** CSV contains headers like "a", "b", "c"
- **THEN** system SHALL treat them as if no headers exist

#### Scenario: CSV with no headers
- **WHEN** CSV has no headers (first row is data)
- **THEN** system SHALL treat the first row as data
- **AND** assign temporary names like "col_1", "col_2"

### Requirement: AI column inference
The system SHALL use AI to analyze column data and suggest meaningful column names based on data patterns.

#### Scenario: AI successfully infers column meaning
- **WHEN** AI analyzes a column with date patterns like "2024-01", "2024-02"
- **THEN** AI SHALL suggest column name "date" or "날짜"

#### Scenario: AI detects numeric column
- **WHEN** AI analyzes a column with numeric values like "100", "150", "200"
- **THEN** AI SHALL suggest column name "sales" or "매출"

#### Scenario: AI detects categorical column
- **WHEN** AI analyzes a column with repeated string values like "Seoul", "Busan", "Daegu"
- **THEN** AI SHALL suggest column name "region" or "지역"

### Requirement: User column name modification
The system SHALL allow users to modify AI-inferred column names through conversation.

#### Scenario: User corrects column name
- **WHEN** user says "col_2는 매출이 아니라 비용이야"
- **THEN** system SHALL update the column name to "cost" or "비용"
- **AND** confirm the change to the user

### Requirement: Data type detection
The system SHALL detect data types for each column: Date, Number, Category, Boolean.

#### Scenario: Date type detection
- **WHEN** column contains values matching date patterns (YYYY-MM-DD, MM-DD-YYYY, Unix timestamp)
- **THEN** system SHALL mark that column as Date type

#### Scenario: Number type detection
- **WHEN** column contains only numeric values (with optional currency symbols or commas)
- **THEN** system SHALL mark that column as Number type

#### Scenario: Category type detection
- **WHEN** column contains string values with low cardinality (unique values < 10% of total rows)
- **THEN** system SHALL mark that column as Category type
