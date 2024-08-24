# 🎨 Banner Module

## Overview

The Banner Module (`banner.py`) handles the visual elements of the CLI interface, including the welcome banner and separators.

## Key Features

1. **Welcome Banner**: Generates a colorful ASCII art banner.
2. **Custom Greeting**: Personalizes the welcome message with the user's name.
3. **Visual Separators**: Creates aesthetic separators between interactions.

## Main Functions

### `setup_console()`

Initializes and returns a `rich.console.Console` object for styled output.

### `print_welcome_banner(console, username)`

Displays a colorful welcome banner with the user's name.

### `print_separator(console)`

Prints a visually appealing separator line.

## Why a Separate Module?

The banner module is separated to:
1. Isolate visual and aesthetic components.
2. Allow for easy customization of the CLI's appearance.
3. Keep the main application logic clean and focused.

## What Makes It Special?

- Uses `rich` library for colorful and styled console output.
- Implements custom ASCII art for a unique and engaging user interface.
- Provides easy-to-use functions for consistent styling across the application.

This module enhances the user experience by providing visual flair and clear demarcation between different parts of the interaction, making the CLI feel more like a polished application.
