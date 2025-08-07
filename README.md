# Static HTML Course - Static Site Generator

A complete static site generator built in Python that converts Markdown files into HTML pages with proper templating and styling.

## Features

- **Markdown to HTML Conversion**: Full markdown parsing with support for headers, paragraphs, lists, code blocks, quotes, and inline formatting (bold, italic, code, links, images)
- **Recursive Page Generation**: Automatically processes entire content directories while preserving folder structure
- **Template System**: Uses HTML templates with placeholder replacement for consistent page layouts
- **Configurable Base Path**: Support for custom base paths for deployment to subdirectories (e.g., GitHub Pages)
- **Static File Copying**: Copies CSS, images, and other static assets to the output directory
- **GitHub Pages Ready**: Built-in support for GitHub Pages deployment with proper path configuration
- **Comprehensive Testing**: 160+ unit tests covering all functionality

## Project Structure

```
├── src/                    # Python source code
│   ├── main.py            # Main entry point
│   ├── textnode.py        # Text node representation
│   ├── htmlnode.py        # HTML node representation
│   ├── split_nodes.py     # Text splitting utilities
│   ├── extract_markdown.py # Markdown element extraction
│   ├── markdown_blocks.py # Block-level markdown parsing
│   ├── text_to_html.py    # Text to HTML conversion
│   ├── extract_title.py   # Title extraction from markdown
│   ├── generate_page.py   # Page generation functions
│   ├── copy_static.py     # Static file copying
│   └── test_*.py          # Unit tests
├── content/               # Markdown content files
│   ├── index.md          # Homepage content
│   ├── blog/             # Blog posts
│   └── contact/          # Contact page
├── static/               # Static assets (CSS, images)
├── template.html         # HTML template
├── docs/                 # Generated output (created during build)
└── README.md            # This file
```

## Usage

### Generate the Site

#### For Local Development
Run the main script to generate the site with default "/" base path:

```bash
python src/main.py
```

Or use the provided shell script:

```bash
./main.sh
```

#### For Production (GitHub Pages)
Run the build script to generate the site with the correct base path for GitHub Pages:

```bash
./build.sh
```

#### Custom Base Path
You can specify a custom base path as a command line argument:

```bash
python src/main.py "/my-custom-path/"
```

This will:
1. Copy all static files from `static/` to `docs/`
2. Process all markdown files in `content/` recursively
3. Generate HTML pages using `template.html` with the specified base path
4. Preserve the directory structure in the output

### Run Tests

Run the comprehensive test suite:

```bash
python -m unittest discover -s src -p "test_*.py"
```

Or use the test script:

```bash
./test.sh
```

## How It Works

1. **Markdown Parsing**: Converts markdown text into structured text nodes
2. **Block Processing**: Identifies and processes different markdown block types (headers, paragraphs, lists, etc.)
3. **HTML Generation**: Converts parsed markdown into HTML nodes
4. **Template Processing**: Injects generated content into HTML templates
5. **File Generation**: Writes HTML files with proper directory structure

## Key Components

- **TextNode**: Represents text with formatting information
- **HTMLNode**: Represents HTML elements and attributes
- **Block Classification**: Identifies markdown block types (header, paragraph, list, etc.)
- **Recursive Generation**: Processes entire content directories automatically
- **Title Extraction**: Automatically extracts page titles from H1 headers

## GitHub Pages Deployment

This project is configured for easy deployment to GitHub Pages:

1. **Build for Production**: Run `./build.sh` to generate the site with the correct base path
2. **Enable GitHub Pages**: Go to your repository settings → Pages → Set source to "Deploy from a branch" → Select "main" branch and "/docs" folder
3. **Access Your Site**: Your site will be available at `https://USERNAME.github.io/REPO_NAME/`

The build script automatically configures all URLs to work with GitHub Pages' subdirectory structure.

## Development

The project follows test-driven development practices with comprehensive unit testing for all functionality. Each module has corresponding test files that validate the implementation.

## Generated Output

The generator creates a complete static website in the `docs/` directory with:
- All markdown files converted to HTML
- Proper navigation structure
- CSS styling applied
- Images and assets copied
- SEO-friendly page titles

## Example Content

The project includes sample content demonstrating:
- Homepage with introduction
- Blog posts with different topics
- Contact page
- Nested directory structures
- Various markdown formatting examples
