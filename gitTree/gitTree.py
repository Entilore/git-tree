#!/usr/bin/env python
# -*- coding: utf-8 -*-

import display
import compute
import click


@click.command()
@click.option('--output', "-o", help='Output file.')
def main(output):
    if compute.isOnGitRepository():
        group = compute.getFileListWithGit()
    else:
        group = compute.getFileListWithoutGit()
    display.display(group, output)


if __name__ == '__main__':
    main()
