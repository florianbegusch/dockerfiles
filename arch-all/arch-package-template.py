#!/usr/bin/env python3

import os
from jinja2 import Environment, FileSystemLoader


# Load jinja template file
TEMPLATE_FILE = 'Dockerfile.template'
template_loader = FileSystemLoader(searchpath='.')
template_env = Environment(loader=template_loader)
template = template_env.get_template(TEMPLATE_FILE)


arch_pkgs = []
filename_pkg_explicit_internal = os.environ['HOME'] \
    + '/Documents/misc/arch/packages_explicit_internal'
with open(filename_pkg_explicit_internal) as f:
    content = f.read()
    arch_pkgs.extend(content.split('\n'))
    del content

filename_pkg_explicit_external = os.environ['HOME'] \
    + '/Documents/misc/arch/packages_explicit_external'
with open(filename_pkg_explicit_external) as f:
    content = f.read()
    arch_pkgs.extend(content.split('\n'))
    del content

filename_exclusions = os.environ['HOME'] \
    + '/Documents/misc/arch/arch-all-docker-image-package-exclusions.txt'
with open(filename_exclusions) as f:
    content = f.read()
    exclusions = content.split('\n')[:-1]
    del content
# print(f'{exclusions=}')


def item_included(item, exclusions):
    for exclusion in exclusions:
        if item.startswith(exclusion):
            return False
    return True


tmp_split = []
# print(f'{arch_pkgs=}')
for item in arch_pkgs:
    if item_included(item, exclusions) and item:
        tmp_split.append(item)
        # print(f'DEBUG included: {item}')
    # else:
        # print(f'DEBUG excluded: {item}')
# print(f'{tmp_split=}')
arch_pkgs = tmp_split
del tmp_split


with open('Dockerfile', 'w') as f:
    f.write(template.render( arch_pkgs=' '.join(arch_pkgs) ))

