# Ship Surroundings Monitoring and Diagnosis App

This application collects data from multiple sensors on a ship, including radar, sonar, thermal, and weather sensors. It processes the data to provide diagnoses about surrounding ships and submarines, evaluating their level of hostility and danger. The application utilizes several technologies, including MQTT, SQL, MongoDB, Kafka, and Neo4j, to efficiently handle real-time data and provide accurate analysis.

## Features
- Collects and processes data from multiple ship sensors:
  - **Radar**: Detects nearby objects, ships, and submarines.
  - **Sonar**: Monitors underwater environments for nearby submarines or underwater objects.
  - **Thermal Sensors**: Detects heat signatures to identify potential threats, including submarines.
  - **Weather Sensors**: Gathers environmental data for context-based analysis.

- Provides real-time diagnosis and analysis on the surrounding ships and submarines:
  - **Hostility Level**: Determines the potential threat of nearby ships or submarines based on behavior and proximity.
  - **Danger Level**: Assesses the level of danger posed by surrounding ships and submarines.

- Real-time data streaming using **MQTT**.
- Stores raw sensor data in **MongoDB** as a data lake for unstructured and semi-structured data.
- Stores structured data in **SQL** for querying and reporting.
- Processes events and performs data analytics using **Kafka**.
- Stores relationships and interactions between ships and submarines in **Neo4j**.

## Technology Stack

_- **MQTT**: Lightweight messaging protocol for real-time data streaming.
- **SQL**: For structured data storage and querying.
- **MongoDB**: Data lake for storing raw, unstructured sensor data.
- **Kafka**: For event streaming and processing of real-time data.
- **Redis**: Temporarily stores data for quick access and analysis.
- **Neo4j**: For managing and querying relationships between ships, submarines, and their surroundings.

## Installation

### Prerequisites
- Python 3.x
- Docker (for containerized services like Kafka, MQTT, and Neo4j)

### Step 1: Clone the Repository
Clone the repository to your local machine.

```bash
git clone https://github.com/Mmhhm/OceanVision.git
