# corvid

corvid is an opinionated simple static site generator.

It processes Markdown files, static assets and directories producing a 1:1
heiarchy of compiled content.

It includes a reloadable local development server, supports custom markdown frontmatter and Jinja templates.

## Installation

```
$ pip install corvid
```

## Running

By default corvid expects to be run in a directory with an `input` directory. With no parameters, corvid will process all files in this directory into the `output` directory, and exit.

```
$ corvid --help
Usage: corvid [OPTIONS]

Options:
  -l, --listen          Enable live reloading
  -b, --bind TEXT       Host to bind to
  -p, --port INTEGER    Port to run on
  -i, --input TEXT      Input directory
  -o, --output TEXT     Output directory
  -t, --templates TEXT  Templates directory
  --help                Show this message and exit.
```

## Example

Given the following directory layout:

```
├── input
│   └── index.md
└── templates
    └── default.html
```
With the following file contents:

`input/index.md`
```
---
title: This is the Index
---

Welcome
```

`templates/default.html`
```html
<html>
    <head>
        <title>{{ title }}</title>
    <body>
        {{ content }}
    </body>
</body>
```

Running `corvid` will produce the additional `output` directory:

```
.
├── input
│   └── index.md
├── output
│   └── index.html
└── templates
    └── default.html
```

And the contents of the file will be:

`output/index.html`
```html
<html>
    <head>
        <title>This is the Index</title>
    <head>
    <body>
        <p>Welcome</p>
    </body>
</body>
```

## Using templates

Custom templates can be set by specifying the path to the template inside the `templates` directory as the `template` frontmatter.

See [`/example`](/example) for a full example.
