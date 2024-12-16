# Reddit Comment Scraper 🧑‍💻🐍

## Overview 📋

The **Reddit Comment Scraper** is a Python script that collects posts and comments from various popular subreddits, including titles, comment text, authors, and the hierarchical relationships between parent and child comments. It recursively fetches all comments, including nested replies, and stores the data in a CSV file for analysis, reporting, or further processing. This project uses a robust backoff strategy for rate-limiting errors and handles network issues gracefully.

---

### Why Use This? 🤔

This scraper can be useful for:

- **Data Analysis** 📊: Analyzing trends in discussions across different communities.
- **Sentiment Analysis** 💬: Scraping and analyzing public sentiment from subreddit comments.
- **Research** 📚: Gathering comment data for academic or market research.

---

## Features 🚀

- **Post Scraping** 📥: Fetches the latest posts from popular subreddits.
- **Recursive Comment Scraping** 🔄: Collects both direct comments and replies in a nested structure.
- **Exponential Backoff** ⏳: Handles rate-limiting (HTTP 429 errors) with retries, preventing script failure due to high traffic or request limits.
- **Data Saving** 💾: Saves scraped data into a well-structured CSV file for easy data manipulation and analysis.
- **Customizable** ⚙️: Easily configurable for adding new subreddits or tweaking scraping parameters.

---

## Supported Subreddits 📚

Currently, the script is configured to scrape the following subreddits:

- `/r/datascience` 📊
- `/r/3d_printing` 🖨️
- `/r/consumer_electronics` 📱
- `/r/diy_electronics` 🔧
- `/r/programming` 💻
- `/r/software_and_apps` 📱
- `/r/streaming_services` 📺

You can modify the `categories` list in the script to add more subreddits. ✨

---

## Requirements 🛠️

To run this script, ensure you have the following Python packages installed:

- **httpx** 🌐: For asynchronous HTTP requests (handles network calls).
- **pandas** 📊: For data manipulation and saving to CSV.
- **logging** 📜: For logging execution status and errors.

---

## Installation ⚙️

Follow these steps to get the script up and running on your local machine.

### 1. Clone the Repository 🚪

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/your-username/reddit-comment-scraper.git
cd reddit-comment-scraper
