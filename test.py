# app.py
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView

app = QApplication(sys.argv)

view = QWebEngineView()

# Load HTML with TailwindCSS via CDN
html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>PyQt Tailwind App</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
  <div class="bg-white p-10 rounded shadow-lg text-center">
    <h1 class="text-3xl font-bold text-blue-600 mb-4">Hello from PyQt + Tailwind!</h1>
    <p class="text-gray-700 mb-6">This is a fully styled HTML UI inside a Python app.</p>
    <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            onclick="alert('Button clicked!')">
      Click Me
    </button>
  </div>
</body>
</html>
"""

view.setHtml(html)
view.setWindowTitle("PyQt Tailwind App")
view.resize(800, 600)
view.show()

sys.exit(app.exec_())
