# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

## 0.3.3 - 2022-05-17

This release only adds Wagtail 3.0 to supported versions due to a versioning
scheme change.

## 0.3.2 - 2022-03-31
### Changed
- Collapse `ColumnsBlock.columns` by default

## 0.3.1 - 2021-10-04
### Fixed
- Format the value for and from forms in stylized blocks to fix the page preview

## 0.3.0 - 2021-08-17
### Added
- CSSClassMixin to define CSS classes of a block at initialization or in its
  meta through `css_class`
- StylizedStructBlock to define an element with different styles in a generic
  way at initialization or in its properties through `styles`

### Changed
- Ease ColumnsBlock subclassing by searching for the sub-block's definition of
  a column in `Meta.column_block`
- Inherit ButtonBlock from StylizedStructBlock to accept optional styles
- Move the columns definition at first in ColumnsBlock
- Always define the `target` block of a LinkBlock

## 0.2.1 - 2021-03-11
### Changed
- Improve Makefile documentation and targets with release facilities

## 0.2.0 - 2021-03-10
### Added
- ColumnsBlock with optional horizontal alignment
- Factories for HeadingBlock and ParagraphBlock to ease tests using
  [wagtail-factories](https://pypi.org/project/wagtail-factories/)

### Changed
- Display image in a centered block in the default template

## 0.1.0 - 2021-03-05
### Added
- HeadingBlock, ParagraphBlock, ButtonBlock and ImageBlock blocks with
  Bootstrap 5 templates
- French translations
