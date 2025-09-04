# Scripts Directory

This directory contains utility scripts for MD2PDF maintenance and setup.

## Scripts to Keep

### setup_assets.py
**Purpose**: Downloads optional Twemoji assets for offline emoji rendering  
**Usage**: Run during initial setup or to update emoji assets
**Keep**: YES - Essential for user setup

### example.py  
**Purpose**: Demonstrates usage of the MD2PDF converter with different styles
**Usage**: Reference for developers and users
**Keep**: YES - Useful documentation/example

## Scripts to Archive/Remove

These scripts were used during Week 1 development and are no longer needed in the main repository:

### add_copyright_headers.py
**Purpose**: One-time script to add copyright headers to Python files
**Status**: Task completed - all headers added
**Action**: REMOVE - No longer needed

### select_core_fonts.py
**Purpose**: One-time script to select and copy core fonts from full set
**Status**: Task completed - core fonts selected and copied
**Action**: REMOVE - No longer needed

### update_css_fallbacks.py
**Purpose**: One-time script to add Google Fonts imports to CSS files
**Status**: Task completed - all CSS files updated
**Action**: REMOVE - No longer needed

## Recommendation

Keep only:
- `setup_assets.py` - Needed for user setup
- `example.py` - Useful for documentation

Move development scripts to an archive or remove them entirely since the tasks are complete.