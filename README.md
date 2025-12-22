# NewsHub Backend API

A robust, scalable RESTful API built with Python and Django, designed to power modern news platforms. This backend handles everything from complex content categorization to social interactions and algorithmic scoring for trending content.

---

## 🚀 Key Features

### 📰 Content Discovery
* **Granular Retrieval:** Fetch articles filtered by **Region**, **Category**, or **Tag**.
* **Algorithmic Sorting:**
    * **Trending Score:** Periodically calculated based on recent engagement.
    * **Editorial Heat:** High-priority content curated by the editorial team.
* **Media Support:** Built-in handling for news-related assets and metadata.

### 👤 User Systems & Social
* **Advanced Profiles:** Full profile customization and UI preference storage.
* **Social Graph:** Follow/unfollow mechanics for other users.
* **Interactions:**
    * React to articles and community posts.
    * Bookmark articles for later reading.
    * Follow specific Tags or Categories to personalize feeds.
* **Social Sharing:** Create posts to share news and react to community updates.

---

## 🛠 Tech Stack

* **Language:** Python 3.12.0
* **Framework:** Django
* **API:** RESTful API
* **Database:** SQLite
* **Task Queue:** Celery (For periodic score calculations)

---

## 🏁 Getting Started

### 1. Prerequisites
* Python 3.10+
* pip / venv

### 2. Installation
```bash
# Clone the repository
git clone [https://github.com/yourusername/newshub-backend.git](https://github.com/yourusername/newshub-backend.git)
cd newshub-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
