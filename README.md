# Instagram Automation
This project automatically creates and uploads Instagram Reels based on the popular "Showerthoughts" niche. It pulls unique content from the Showerthoughts subreddit, transforms it into engaging short-form videos, and posts them directly to Instagram, automating the entire content creation process.

## Table of Contents
- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)

## Introduction
I created this project in January 2024 in response to the growing trend of earning money online through short-form content. Many creators were manually using tools to produce hundreds of Instagram Reels per hour and scheduling them for maximum engagement. I realized that this process could be fully automated, making it easier and faster for users to generate and post high-quality content. This project is designed to handle the entire workflow—from content creation to uploading—saving both time and effort.



## Installation
1. Clone the repository

```bash
git clone https://github.com/Muzzamil-codes/Instagram-Automation.git
```

2. Install dependecies

```bash
pip install -r requirements.txt
```

## Usage

1. Create a pro_secrets.py file and write the following in it:
```python
insta_credentials = {"username": "Enter your instagram's username", "password":"Enter your instagram's password"}
reddit_credentials = {"client_id": "Enter your reddit api client id", "secret_key":"Enter reddit api client secret", "username":"Username of your reddit account", "password":"your api password"}
DIScord_webhook = r"Your discord webhook link"
```
2. Run the following on your Command line:
```bash
python showerthoughtgen.py
```