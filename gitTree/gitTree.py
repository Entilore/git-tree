#!/usr/bin/env python
# -*- coding: utf-8 -*-

import display
import compute
import click


@click.command()
@click.option('--output', "-o", help='Output file.')
@click.option('--ignore', '-i', help='Ignore files matching this regex', default="")
def main(output, ignore):
    if compute.isOnGitRepository():
        group = compute.getFileListWithGit(ignore)
    else:
        group = compute.getFileListWithoutGit(ignore)
    display.display(group, output)


if __name__ == '__main__':
    main()
