# 🐦 tierlesstweet

Generate high-quality, engaging Twitter (X) posts and matching AI-generated images based on your content's tone — whether it's for casual users, blue-tick professionals, or golden-tick brands.

[🌐 Live Demo](https://tierlesstweet.onrender.com)

---

## 🚀 Features

* ✍️ **AI-Generated Tweets**
  Uses **Gemini 2.5 Flash** to craft single-post tweets tailored to different Twitter tiers:

  * **No Tick**: Short, punchy tweets under 280 characters.
  * **Blue Tick**: Polished posts under 2500 characters.
  * **Golden Tick**: In-depth, authoritative content without character limits.

* 🎨 **AI-Generated Images**
  Uses **Nebius AI Studio (Flux Schnell)** to generate a unique image that matches the tweet content.

* 🔍 **Clean Output**
  Tweets are stripped of markdown formatting to ensure clean, platform-ready output.

* 📁 **Auto-Save**
  Images are saved and served from the `/static/generated_images` directory.

---

## 🛠️ Tech Stack

* **Backend**: Python, Flask
* **LLM**: Google Generative AI (Gemini 2.5 Flash)
* **Image Generator**: Nebius AI Studio (Flux Schnell)
* **Deployment**: Render

---

## 📸 Preview

![Example Screenshot](static/example_preview.png)

> *Demo of tweet and image generation interface.*

---

## 📂 Project Structure

```
tierlesstweet/
│
├── static/
│   └── generated_images/
├── templates/
│   └── index.html
├── .env
├── app.py
└── README.md
```

---

## 🔧 Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/tierlesstweet.git
   cd tierlesstweet
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file and add your API keys:

   ```env
   GENAI_API_KEY=your_google_genai_key
   NEBIUS_API_KEY=your_nebius_api_key
   ```

5. **Run the App**

   ```bash
   python app.py
   ```

6. **Open in Browser**
   Navigate to `http://127.0.0.1:5000` in your browser.

---

## 🧠 How It Works

1. User inputs keywords and selects a tweet type (No Tick, Blue Tick, Golden Tick).
2. A prompt is built and passed to the Gemini model.
3. The resulting tweet is cleaned and passed as a prompt to the Nebius image model.
4. The tweet and its matching AI-generated image are displayed together.

---

## ✨ Future Improvements

* User authentication and history tracking
* Option to download tweet + image as a bundle
* Twitter API integration for direct posting
* Dark mode UI and mobile responsiveness

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 👨‍💼 Author

Made with ❤️ by [Abhiraj Adhikary](https://github.com/abhirajadhikary06) and [Anik Chand](https://github.com/anikchand461) 
