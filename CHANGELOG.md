# Changelog

All notable changes to the Linkup CLI are documented in this file.

## [0.5.0] - 2025-03-22

### Added
- **Clipboard mode** (`--clipboard` / `-c`): Read query directly from system clipboard
- **File mode** (`--file` / `-f`): Read query from a file
- **Interactive mode**: When no query provided, prompts user to paste text and submit with Ctrl+D
- Cross-platform clipboard support (macOS, Linux, Windows)

### Why
Multi-line prompts are critical for Linkup to work properly. Shell command lines don't handle multi-line input well, so these new modes allow users to paste complex prompts.

## [0.4.1] - 2025-03-22

### Added
- Stdin support: Pipe content directly to linkup (`echo "query" | linkup search`)

## [0.4.0] - 2025-03-22

### Added
- `linkup setup` command for interactive onboarding
- Opens browser to get API key
- Saves API key securely to `~/.linkup/config` with 600 permissions
- Tests connection after setup

## [0.3.3] - 2025-03-22

### Added
- Friendly error messages for common issues:
  - 403 Forbidden (proxy/firewall/sandbox)
  - 401 Unauthorized (invalid API key)
  - 404 Not Found (URL issues)
  - Timeout errors

## [0.3.2] - 2025-03-22

### Fixed
- `linkup fetch` now correctly uses `.markdown` attribute instead of `.content`

## [0.3.1] - 2025-03-22

### Fixed
- Version display now shows correct version
- Updated repository URLs in pyproject.toml

## [0.3.0] - 2025-03-22

### Added
- `fast` depth option (quickest, no LLM processing)

## [0.2.0] - 2025-03-22

### Added
- `--depth` flag: `fast`, `standard`, `deep`
- `--output` flag: `sourcedAnswer`, `searchResults`

## [0.1.0] - 2025-03-22

### Added
- Initial release
- `linkup search` command
- `linkup fetch` command
- `linkup config` command
- API key configuration via environment variable or config file

---

*This CLI was developed with assistance from Claude Code.*
