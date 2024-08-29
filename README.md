# AI-Powered CSV Visualizer

## Overview

**AI-Powered CSV Visualizer** is a FastAPI-based web application that allows users to upload CSV files, generate a summary of the dataset, and create custom visualizations through natural language prompts using a Generative Language Model (LLM). This project leverages the power of AI to simplify the process of data exploration and visualization.

## Features

- **CSV Upload**: Upload any CSV file and instantly generate a statistical summary.
- **AI-Powered Plotting**: Generate complex data visualizations through simple text prompts using a Generative Language Model (LLM).
- **In-Browser Display**: View the generated plots directly in the browser without needing any additional software.
- **User-Friendly Interface**: Clean, responsive design for a smooth user experience.

## Screenshots

### 1. Upload CSV File

Upload your CSV file to the application to get started.

![Upload CSV](https://github.com/karthickeyan17/Smart_Visualizer/blob/main/screenshots/1.png)

### 2. View Data Summary

After uploading, you will see a summary of the dataset with various statistical details.

![Data Summary](https://github.com/karthickeyan17/Smart_Visualizer/blob/main/screenshots/2.png)

### 3. Generate Visualizations

Input a natural language prompt to generate visualizations based on your data.

![Generate Visualizations](https://github.com/karthickeyan17/Smart_Visualizer/blob/main/screenshots/3.png)

## Technologies Used

- **FastAPI**: For building the web application.
- **Jinja2**: For templating and rendering HTML.
- **Pandas**: For data manipulation and summary generation.
- **Matplotlib**: For generating plots.
- **Google Generative AI (Gemini 1.5 Flash)**: For interpreting user prompts and generating plotting code.
- **Base64 Encoding**: For in-memory plot display.

## Installation

### Prerequisites

- Python 3.8+
- A Google API key for the Generative AI (Gemini 1.5 Flash) model.
