# GitHub Profile Widget Service

Dynamic SVG widget service for GitHub profile that updates in real-time.

## Features

- 🕐 Live Barcelona & New York time
- 🌤️ Real-time Barcelona weather
- ⚡ Updates on every page visit
- 🚀 Zero GitHub commits needed

## Deploy to Render.com

1. Push this directory to a GitHub repository
2. Go to [render.com](https://render.com) and create a new Web Service
3. Connect your GitHub repo
4. Select the `github-widget-service` folder as root directory
5. Render will auto-detect the `render.yaml` configuration
6. Deploy!

Your widget will be available at: `https://your-service.onrender.com/widget.svg`

## Local Testing

```bash
pip install -r requirements.txt
python app.py
```

Visit: http://localhost:5000/widget.svg

## Usage in GitHub README

Once deployed, update your README.md:

```markdown
<a href="https://wttr.in/Barcelona">
  <img src="https://your-service.onrender.com/widget.svg" alt="Barcelona Live Time & Weather" />
</a>
```

## API Endpoints

- `GET /widget.svg` - Returns the live SVG widget
- `GET /health` - Health check endpoint
