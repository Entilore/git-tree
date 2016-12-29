#!/usr/bin/env python
# -*- coding: utf-8 -*-

import display
import compute
import click
import os


@click.command()
@click.option('--output', "-o", help='Output file.')
@click.option('--ignore', '-i', help='Ignore files matching this regex', default="")
@click.argument("path",  type=click.Path(exists=True), required=False)
def main(output, ignore, path):
    if path:
        if output:
            output = os.path.join(os.getcwd(), output)
        os.chdir(path)

    if compute.isOnGitRepository():
        group = compute.getFileListWithGit(ignore)
    else:
        group = compute.getFileListWithoutGit(ignore)
    display.display(group, output)


if __name__ == '__main__':
    main()
