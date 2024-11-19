# Fiorino.AI

Fiorino.AI is an open-source solution that enables SaaS services using Large Language Models (LLMs) to track costs, usage, and bill customers efficiently.

## Key Features

- **Open Source**: Encourages community adoption and collaboration.
- **Flexible Integration**: Supports various LLM services and models.
- **Detailed Tracking**: Anonymous user-specific metrics and cost tracking.
- **Modular Billing**: Integration with billing systems (e.g., Stripe) for direct user billing.
- **Privacy-First**: Uses anonymous IDs to protect user privacy.
- **Scalable Architecture**: Designed to handle multiple realms without performance degradation.
- **Customization**: Advanced options for realm-specific themes and dashboards.
- **Interoperability**: Optional data sharing between authorized realms.
- **Audit and Compliance**: Comprehensive audit trails for each realm.

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
