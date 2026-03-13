# ergoCub Software Documentation Migration to Zensical

This document summarizes the migration of the ergoCub Software documentation from mkdocs to zensical format.

## Changes Made

### 1. **mkdocs.yml** - Updated Configuration
- **Added autorefs plugin**: Enables automatic reference resolution
- **Updated Material Theme**: Added modern features like:
  - `announce.dismiss` - Dismissible announcement banner
  - `navigation.instant` - Instant navigation without full page reloads
  - `navigation.footer` - Footer navigation
  - `content.code.copy` & `content.code.select` - Code copying features
  - Modern icon theme with lucide icons
- **Updated markdown extensions**: Added `md_in_html` and `footnotes`
- **Removed mkdocs-video plugin**: Functionality can be handled through standard HTML/markdown
- **Updated magiclink configuration**: Points to ergocub-software repo for proper linking

### 2. **doc/mkdocs/site-compile.sh** - Build Script
Changed from:
```bash
mkdocs build -c -v --site-dir doc/mkdocs/site
```
To:
```bash
zensical build --clean
```

### 3. **.github/workflows/gh-pages.yml** - CI/CD Pipeline
- Replaced `mkdocs` and `mkdocs-material` with `zensical` and `mkdocs-autorefs`
- Removed `mkdocs-video` dependency (no longer needed)
- Added `--break-system-packages` flag for pip install

### 4. **requirements.txt** - New Dependency File
Created to list Python dependencies:
- `zensical` - Documentation server/builder
- `mkdocs-autorefs` - Automatic reference plugin
- `pymdown-extensions` - Additional Markdown extensions

### 5. **.devcontainer/** - Dev Container Setup
- **Dockerfile**: Complete development environment with all dependencies
- **devcontainer.json**: VS Code dev container configuration for easy local development

## Local Usage

### Option 1: Using Zensical Directly
```bash
# Install dependencies
pip install -r requirements.txt

# Serve documentation locally
zensical serve

# Build documentation
zensical build
```

### Option 2: Using Docker Dev Container
```bash
# VS Code will detect the dev container automatically
# Open in Dev Container -> Rebuild Container
```

## Key Benefits of Zensical
1. **Modern Python-based docs server** built on MkDocs
2. **Automatic reference resolution** through autorefs plugin
3. **Modern Material theme features** with better UX
4. **Better instant navigation** for faster page loads
5. **Consistent setup** with the documentation repository

## Testing
Before committing changes:
```bash
# Build locally
zensical build --clean

# Serve and test
zensical serve
# Visit http://localhost:8000
```

## Notes
- The nav structure remains unchanged
- All existing documentation files work without modification
- Doxygen documentation generation is still included in the CI/CD pipeline
- The output site structure is preserved for GitHub Pages deployment
