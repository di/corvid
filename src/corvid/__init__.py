import time
import os
import pathlib
import glob
import shutil

import click
import frontmatter
import markdown
import jinja2


def render_markdown(env, input_path, output_path):
    md = markdown.Markdown()
    file_parts = frontmatter.load(input_path)

    context = {**file_parts.metadata, "content": md.convert(file_parts.content)}

    try:
        template = env.get_template(context.get("template", "default.html"))
    except jinja2.TemplateNotFound:
        # If no template is found, just render the content
        template = env.from_string("{{content}}")

    html = template.render(**context)
    with open(output_path.with_suffix(".html"), "w+") as f:
        f.write(html)


def _build(input, output, templates):
    # Delete any existing output
    shutil.rmtree(output, ignore_errors=True)

    input_paths = [
        pathlib.Path(path) for path in glob.iglob(f"{input}/**", recursive=True)
    ]

    count = 0
    start = time.time()

    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates))

    with click.progressbar(input_paths) as paths:
        for input_path in paths:
            output_path = pathlib.Path(output, *input_path.parts[1:])

            if os.path.isdir(input_path):
                os.mkdir(output_path)
            elif input_path.suffix in {".md", ".markdown", ".mkd", ".mdown"}:
                count += 1
                render_markdown(env, input_path, output_path)
            else:
                count += 1
                shutil.copy(input_path, output_path)

    click.echo(f"Done: Processed {count} files in {time.time()-start:.2f} seconds.")


def _listen(input, output, templates, port, bind, on_modified):
    import http.server
    import socket
    import functools
    import sys

    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler, FileModifiedEvent

    # Set up the event handler
    def _on_modified(event):
        if isinstance(event, FileModifiedEvent):
            click.echo("Changes detected, rebuilding...")
            on_modified()

    my_event_handler = PatternMatchingEventHandler(case_sensitive=True)
    my_event_handler.queue = []
    my_event_handler.on_modified = _on_modified

    # Set up the Watchdog observer
    my_observer = Observer()
    my_observer.schedule(my_event_handler, input, recursive=True)
    my_observer.schedule(my_event_handler, templates, recursive=True)
    my_observer.start()

    infos = socket.getaddrinfo(
        bind, port, type=socket.SOCK_STREAM, flags=socket.AI_PASSIVE
    )
    http.server.ThreadingHTTPServer.address_family, type, proto, canonname, addr = next(
        iter(infos)
    )
    handler_class = functools.partial(
        http.server.SimpleHTTPRequestHandler, directory=output
    )
    handler_class.protocol_version = "HTTP/1.0"
    with http.server.ThreadingHTTPServer(addr, handler_class) as httpd:
        host, port = httpd.socket.getsockname()[:2]
        url_host = f"[{host}]" if ":" in host else host
        click.echo(
            f"Serving HTTP on {host} port {port} " f"(http://{url_host}:{port}/) ..."
        )
        try:
            while True:
                httpd.handle_request()

        except KeyboardInterrupt:
            my_observer.stop()
            my_observer.join()
            click.echo("\nKeyboard interrupt received, exiting.")
            sys.exit(0)


@click.command()
@click.option("-l", "--listen", is_flag=True, help='Enable live reloading')
@click.option("-b", "--bind", default="0.0.0.0", help='Host to bind to')
@click.option("-p", "--port", default=8000, help='Port to run on ')
@click.option("-i", "--input", default="input", help='Input directory')
@click.option("-o", "--output", default="output", help='Output directory')
@click.option("-t", "--templates", default="templates", help='Templates directory')
def cli(listen, port, bind, input, output, templates):
    # Make a build callable
    build = lambda: _build(input, output, templates)

    # Run the buld
    build()

    if listen:
        _listen(input, output, templates, port=port, bind=bind, on_modified=build)
