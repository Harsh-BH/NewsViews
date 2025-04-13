# Local Happenings News Aggregator

A full-stack web application built for the FY25Q2 Internship Assignment. It collects local news via a Google Form, processes the data, and displays it on a public news feed with moderation, filtering, and bookmarking features.

## 📌 Project Overview

This application aims to create a community-driven news aggregator. Local users submit news updates through a Google Form, which are then validated, filtered, and moderated using automated services before being published in a feed inspired by Inshorts.

## 🚀 Hosted Demo

[🔗 Click here to view the live demo](#)  
*(Replace with your actual deployed URL)*

## 📂 GitHub Repository

[🔗 View Source Code on GitHub](#)  
*(Replace with your actual GitHub repo link)*

---

## 🧰 Tech Stack

- **Frontend**: Next.js
- **Backend**: Node.js / Express / Google Sheets API
- **Database**: Google Sheets
- **Image Moderation**: OpenAI GPT-4o API (or similar)
- **Deployment**: Vercel

---

## 🧾 Features

### ✅ Core Features
- **📝 Google Form Integration**: Collects user-submitted news.
- **📊 Google Sheet Storage**: Auto-populates form responses.
- **🧪 Data Validation**: Ensures fields are filled; checks for duplicate submissions using text similarity.
- **🧼 Image Moderation**: Filters out inappropriate images using GPT-4o.
- **📰 News Feed**: Displays news cards with title, image, description, city, topic, and masked phone number.
- **🔍 Filters**: Sort news by **City** or **Topic**.
- **🔖 Bookmarking**: Save stories locally using local storage.

### ⭐ Extra Credit (Optional)
- Live updates (e.g., via polling or WebSockets).
- Analytics dashboard: total news, most popular topics.
- Advanced bookmarks with user login/authentication.

---

## 🔧 Setup Instructions

### 1. Clone the Repo
```bash
git clone https://github.com/Harsh-BH/NewsViews.git
cd NewsViews