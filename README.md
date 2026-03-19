# Linkup CLI

Official command-line interface for [Linkup](https://linkup.so) - AI-powered web search.

## Installation

```bash
pip install linkup-cli
```

## Quick Start

```bash
# Install
pip install linkup-cli

# Setup (opens browser to get API key)
linkup setup

# Search
linkup search "What is the capital of France?"
```

That's it! The setup wizard will guide you through getting your API key.

## Usage

### Search

```bash
# Basic search (standard depth, sourced answer)
linkup search "your query"

# Deep search (more thorough, better for complex queries)
linkup search "complex research topic" --depth deep

# Get raw search results instead of AI answer
linkup search "python tutorials" --output searchResults

# Combine options
linkup search "latest AI research" --depth deep --output searchResults

# Short form
linkup s "your query" -d deep -o searchResults
```

### Fetch

Extract content from any URL:

```bash
linkup fetch "https://example.com"
```

### Configuration

Check your configuration:

```bash
linkup config
```

## Options

| Flag | Short | Values | Description |
|------|-------|--------|-------------|
| `--depth` | `-d` | `fast`, `standard`, `deep` | Search depth (default: standard) |
| `--output` | `-o` | `sourcedAnswer`, `searchResults` | Output type (default: sourcedAnswer) |
| `--version` | `-V` | | Show version |
| `--help` | `-h` | | Show help |

## Environment Variables

| Variable | Description |
|----------|-------------|
| `LINKUP_API_KEY` | Your Linkup API key (required) |

## Examples

```bash
# Quick facts
linkup search "population of tokyo"

# Research
linkup search "latest developments in quantum computing" --deep

# Get sources
linkup search "best python web frameworks" --output searchResults

# Extract article content
linkup fetch "https://example.com/article"
```

## Links

- [Linkup Website](https://linkup.so)
- [Documentation](https://docs.linkup.so)
- [Get API Key](https://app.linkup.so)
- [Python SDK](https://github.com/LinkupPlatform/linkup-python-sdk)

## License

MIT
