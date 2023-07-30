# CourseGenius Backend Service

![CourseGenius Logo](CourseGenius.png)

## Overview

CourseGenius Backend Service is a powerful service that drives the core functionality of the CourseGenius platform, enabling seamless management and delivery of courses.

## Prerequisites

Make sure you have the following software installed before setting up the project:

- **Docker**: The latest version of Docker is required for local development.

## Local Development

### Without Docker

For local development without Docker, you will need the following tools:

- `python3.10.11` (see `pyproject.toml` for the full version)
- `postgresql` with version `15.2`

When developing locally, we recommend using one of the following IDEs:

- `pycharm 2023+`
- `vscode`
- `IntelliJ IDEA 2023+`

### With Docker

For local development with Docker, you will need:

- `docker` latest version

## Getting Started

Follow these steps to get started with CourseGenius Backend Service:

1. Clone the repository: `git clone https://github.com/towhidulhaque/CourseGenius.git`
2. Create the configuration file by copying the template:

cp config/.env.template config/.env

## Development

To start the development server locally using Docker, follow these steps:

1. Copy the `docker-compose.override.template.yml` file as `docker-compose.override.yml`:
   cp docker-compose.override.template.yml docker-compose.override.yml
2. Start the development server and required services:
   docker-compose up
3. Running a command inside the Docker container:
   docker-compose run --rm web [command]

## Documentation

Explore the full documentation in the [`docs/`](docs) directory. It contains detailed information about the project's architecture, API endpoints, and more.

## Contributing

We welcome contributions to make CourseGenius even better! If you want to contribute, please follow our [Contribution Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or feedback, please reach out to us at [contact@coursegenius.com](mailto:contact@coursegenius.com).

---
© 2023 CourseGenius Inc. All rights reserved.
