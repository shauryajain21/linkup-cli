"""Linkup CLI - Search the web with AI from your terminal."""

import argparse
import os
import sys

# Valid options
VALID_DEPTHS = ["fast", "standard", "deep"]
VALID_OUTPUT_TYPES = ["sourcedAnswer", "searchResults"]


def get_client():
    """Initialize and return the Linkup client."""
    api_key = os.environ.get("LINKUP_API_KEY")
    if not api_key:
        print("Error: LINKUP_API_KEY environment variable not set")
        print("Get your API key at https://app.linkup.so")
        print("\nSet it with: export LINKUP_API_KEY='your-key'")
        sys.exit(1)

    from linkup import LinkupClient
    return LinkupClient(api_key=api_key)


def cmd_search(args):
    """Execute a search query."""
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    client = get_client()

    query = " ".join(args.query)
    if not query:
        console.print("[red]Error: No query provided[/red]")
        sys.exit(1)

    # Determine depth
    depth = args.depth or "standard"

    # Determine output type
    output_type = args.output or "sourcedAnswer"

    # Show search parameters
    console.print(f"[dim]Depth: {depth} | Output: {output_type}[/dim]")

    try:
        with console.status(f"[bold blue]Searching...[/bold blue]"):
            response = client.search(
                query=query,
                depth=depth,
                output_type=output_type,
            )
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)

    if output_type == "searchResults":
        # Display search results
        for i, result in enumerate(response.results, 1):
            console.print(f"\n[bold cyan]{i}. {result.name}[/bold cyan]")
            console.print(f"   [dim]{result.url}[/dim]")
            if result.content:
                snippet = result.content[:300] + "..." if len(result.content) > 300 else result.content
                console.print(f"   {snippet}")
    else:
        # Display sourced answer
        console.print()
        console.print(Markdown(response.answer))

        if hasattr(response, "sources") and response.sources:
            console.print("\n[bold]Sources:[/bold]")
            for src in response.sources[:5]:
                console.print(f"  [dim]•[/dim] [link={src.url}]{src.name}[/link]")

    console.print()


def cmd_fetch(args):
    """Fetch and extract content from a URL."""
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    client = get_client()

    try:
        with console.status(f"[bold blue]Fetching {args.url}...[/bold blue]"):
            # render_js=True recommended for JS-heavy sites
            response = client.fetch(url=args.url)

        console.print()
        console.print(Markdown(response.content))
        console.print()
    except Exception as e:
        console.print(f"[red]Error fetching URL: {e}[/red]")
        sys.exit(1)


def cmd_config(args):
    """Show or set configuration."""
    from rich.console import Console
    from rich.table import Table

    console = Console()

    table = Table(title="Linkup CLI Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    api_key = os.environ.get("LINKUP_API_KEY", "")
    masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else "(not set)"

    table.add_row("API Key", masked_key)
    table.add_row("API Key Set", "Yes" if api_key else "[red]No[/red]")

    console.print()
    console.print(table)
    console.print()

    if not api_key:
        console.print("[yellow]To set your API key:[/yellow]")
        console.print("  export LINKUP_API_KEY='your-key'")
        console.print("\nGet your API key at: [link=https://app.linkup.so]https://app.linkup.so[/link]")
        console.print()


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="linkup",
        description="Linkup CLI - AI-powered web search from your terminal",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  linkup search "What is the capital of France?"
  linkup search "Latest AI news" --deep
  linkup search "Python tutorials" --results
  linkup fetch "https://example.com"
  linkup config

Get your API key at: https://app.linkup.so
Documentation: https://docs.linkup.so
        """,
    )
    parser.add_argument(
        "--version", "-V", action="version", version="%(prog)s 0.3.1"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search command
    search_parser = subparsers.add_parser(
        "search", aliases=["s"], help="Search the web"
    )
    search_parser.add_argument("query", nargs="*", help="Search query")
    search_parser.add_argument(
        "--depth", "-d",
        choices=VALID_DEPTHS,
        default="standard",
        help="Search depth: fast (quickest, no LLM), standard (balanced), or deep (most thorough). Default: standard"
    )
    search_parser.add_argument(
        "--output", "-o",
        choices=VALID_OUTPUT_TYPES,
        default="sourcedAnswer",
        help="Output type: sourcedAnswer (AI summary) or searchResults (raw results). Default: sourcedAnswer"
    )
    search_parser.set_defaults(func=cmd_search)

    # Fetch command
    fetch_parser = subparsers.add_parser(
        "fetch", aliases=["f"], help="Fetch and extract content from a URL"
    )
    fetch_parser.add_argument("url", help="URL to fetch")
    fetch_parser.set_defaults(func=cmd_fetch)

    # Config command
    config_parser = subparsers.add_parser(
        "config", aliases=["c"], help="Show configuration"
    )
    config_parser.set_defaults(func=cmd_config)

    # Parse args
    args = parser.parse_args()

    # Handle no command - default to search if args look like a query
    if args.command is None:
        # Check if there are extra args that might be a query
        if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
            # Treat as implicit search
            sys.argv.insert(1, "search")
            args = parser.parse_args()
        else:
            parser.print_help()
            sys.exit(0)

    # Execute command
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
