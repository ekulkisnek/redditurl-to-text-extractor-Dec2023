from flask import Flask, request, render_template_string, redirect, url_for
import praw
import os
import logging
import re  # Import regular expressions

# ------------------------
# Logging Configuration
# ------------------------
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')
logger = logging.getLogger()

# Flask Application Setup
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Initialize PRAW
reddit = praw.Reddit(
    client_id=os.environ.get("REDDIT_CLIENT_ID"), 
    client_secret=os.environ.get("REDDIT_CLIENT_SECRET"), 
    user_agent=os.environ.get("REDDIT_USER_AGENT")
)

# In-memory cache
comments_cache = {}

# Function to extract thread ID from URL
def extract_thread_id(url):
    match = re.search(r'/comments/([a-zA-Z0-9_]+)', url)
    return match.group(1) if match else None

# Route: Display Comments and Original Post
@app.route('/comments/<thread_id>')
def show_comments(thread_id):
    data = comments_cache.get(thread_id, {'title': 'No post available.', 'text': 'No comments available.'})
    return render_template_string('''
        <style>
            #content {
                white-space: pre-wrap;
            }
        </style>
        <button onclick="copyToClipboard()">Copy to Clipboard</button>
        <script>
        function copyToClipboard() {
            var text = document.getElementById("content").innerText;
            navigator.clipboard.writeText(text);
        }
        </script>
        <h1>{{ data.title }}</h1>
        <pre id="content">{{ data.text }}</pre>
        <a href="/">Back to form</a>
        ''', data=data)

# Route: Main Index
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        thread_id = extract_thread_id(url)
        if thread_id:
            submission = reddit.submission(id=thread_id)
            submission.comments.replace_more(limit=None)
            comments = '\n\n'.join(comment.body for comment in submission.comments.list())

            # Combine post title, body, and comments
            full_text = f"Title: {submission.title}\n\n{submission.selftext}\n\nComments:\n\n{comments}"

            # Store in cache
            comments_cache[thread_id] = {
                'title': submission.title,
                'text': full_text
            }
            return redirect(url_for('show_comments', thread_id=thread_id))
        else:
            return render_template_string('<p>Invalid URL. Please enter a valid Reddit thread URL.</p><a href="/">Back to form</a>')

    return render_template_string('''
        <form method="post">
            Reddit Thread URL: <input type="text" name="url"><br>
            <input type="submit" value="Submit">
        </form>
        ''')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080, debug=True)
