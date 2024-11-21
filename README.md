# Fiorino.AI

## Know your AI costs, maximize profits

[Fiorino.AI](https://fiorinoai.tech) is an open-source solution that helps SaaS owners track and optimize their AI costs. Monitor per-user LLM usage, set spending limits, and automate usage-based billing.

## Overview

Fiorino.AI empowers SaaS businesses using Large Language Models (LLMs) by providing comprehensive cost tracking, usage monitoring, and automated billing solutions. Whether you're using OpenAI, Anthropic, or any other LLM provider, Fiorino.AI helps you understand and optimize your AI spending while ensuring profitability.

## Key Features

- [x] **Open Source**: Encourages community adoption and collaboration.
- [x] **Flexible Integration**: Supports various LLM services and models.
- [x] **Detailed Tracking**: Anonymous user-specific metrics and cost tracking.
- [ ] **Modular Billing**: Integration with billing systems (e.g., Stripe) for direct user billing.
- [x] **Privacy-First**: Uses anonymous IDs to protect user privacy.
- [x] **Scalable Architecture**: Designed to handle multiple realms without performance degradation.
- [ ] **Audit and Compliance**: Comprehensive audit trails for each realm.
- [ ] **Usage Limits**: Set and monitor usage limits per user or subscription tier. Get alerts when users approach their quota.
- [ ] **Custom Insights**: Tag LLM interactions with your business metrics. Track costs by feature, action, or any custom dimension. Transform raw usage data into meaningful business intelligence.
- [ ] **AI Cost Analyst**: Chat with your usage data through our AI assistant. Get instant insights, cost optimization suggestions, and usage patterns in natural language. Your personal AI consultant for LLM economics.

![FiorinoAI Cost Usage Dashboard ](https://raw.githubusercontent.com/fiorino-ai/.github/refs/heads/main/images/fiorinoai-screenshoot.png)

## Core Functionality

1. **Message Processing**: Receive and analyze user messages and LLM responses.
2. **Usage Metrics**: Track token usage and associated costs per user.
3. **Cost Management**: Maintain a database of LLM model costs with customizable overhead.
4. **Billing Integration**: Seamless integration with Stripe for usage-based billing.

## Installation

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/Fiorino.AI.git
   cd Fiorino.AI
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up PostgreSQL:

   - Install PostgreSQL if you haven't already
   - Create a new database for Fiorino.AI
   - Update the `DATABASE_URL` in `app/core/config.py` with your PostgreSQL credentials

5. Initialize the database:
   ```
   python run.py
   ```
   This will apply all pending migrations before starting the server.

## Docker Installation

1. Pull the image from Docker Hub:

   ```bash
   docker pull fiorino/fiorino-ai:latest
   ```

2. Run the container:
   ```bash
   docker run -d \
     -p 8000:8000 \
     -e DATABASE_URL="postgresql://user:password@host:5432/db" \
     fiorino/fiorino-ai:latest
   ```

### Build from source

1. Clone the repository:

   ```bash
   git clone https://github.com/fiorino-ai/fiorino-ai.git
   cd fiorino-ai
   ```

2. Build the Docker image:
   ```bash
   docker build -t fiorino/fiorino-ai:latest .
   ```

## Usage

Start the server with:

```
python run.py
```

The server will be available at `http://localhost:8000`. API documentation can be accessed at `http://localhost:8000/docs`.

## Development

To run the server in debug mode:

```
DEBUG=True python run.py
```

### Seed Usage Data

```
DATABASE_URL="..." python -m app.scripts.seed_usage
```

## Testing

Run tests with:

```
pytest
```

## Contributing

We welcome contributions! Feel free to submit a Pull Request or open an Issue to discuss new features or improvements.

## License

This project is released under the MIT License.

## User Management

### Creating a New User

#### Local Environment

To create a new user in the local environment:

```
# Run the create user script from the project root
DATABASE_URL="..." python -m app.scripts.create_user
```

#### Docker Environment

To create a new user in the Docker environment:

```
# If the container is running
docker exec -it <container_name> python -m app.scripts.create_user
# Or using docker-compose
docker-compose exec api python -m app.scripts.create_user
```

The script will:

1. Prompt for an email address
2. Generate a secure random password
3. Create the user in the database
4. Display the generated password (save it securely!)

> **Note**: The generated password will only be shown once during creation. Make sure to save it in a secure location.
