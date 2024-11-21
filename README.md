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

## Quickstart

To make Fiorino.AI run on your machine, you just need [`docker`](https://docs.docker.com/get-docker/) installed:

```bash
   docker run --rm -it \
     -p 8000:8000 \
     -e DATABASE_URL="postgresql://user:password@host:5432/db" \
      ghcr.io/fiorino-ai/fiorino-ai:latest
```

- Access to the dashboard on [localhost:8000/app](http://localhost:8000/app).
- You can also interact via REST API and try out the endpoints on [localhost:8000/docs](http://localhost:8000/docs)

Follow instructions on how to setup Fiorino.AI on [Quickstart Guide](https://github.com/fiorino-ai/fiorino-ai/wiki/Quickstart-Guide).

## Contributing

We welcome contributions! Feel free to submit a Pull Request or open an Issue to discuss new features or improvements.
