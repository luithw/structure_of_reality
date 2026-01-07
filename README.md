# Structure of Reality

**Chinese American computer scientist, navigating to the origin of intelligence.**

A personal blog series exploring artificial intelligence, consciousness, and the fundamental nature of intelligence. Hosted on GitHub Pages with optional Facebook integration.

## 🌟 Features

- **Static Site Generator**: Built with Jekyll for fast, secure, and maintainable blog
- **GitHub Pages Hosting**: Free, reliable hosting with automatic deployments
- **Automated Publishing**: Optional GitHub Actions workflows for Facebook integration
- **Modern Design**: Clean, responsive design optimized for reading
- **SEO Optimized**: Meta tags, Open Graph, and Twitter Card support
- **RSS Feed**: Automatic feed generation for subscribers

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Setup Guide](#setup-guide)
- [Writing Posts](#writing-posts)
- [Publishing Workflow](#publishing-workflow)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### Prerequisites

- Ruby 3.x
- Bundler
- Python 3.8+
- Git
- GitHub account

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/structure_of_reality.git
   cd structure_of_reality
   ```

2. **Install Jekyll dependencies**
   ```bash
   bundle install
   ```

3. **Run local server**
   ```bash
   bundle exec jekyll serve
   ```

4. **View your site**
   Open your browser to `http://localhost:4000`

## 🔧 Setup Guide

### 1. GitHub Repository Setup

1. Create a new GitHub repository named `structure_of_reality`
2. Push this codebase to the repository:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Structure of Reality blog"
   git branch -M main
   git remote add origin https://github.com/yourusername/structure_of_reality.git
   git push -u origin main
   ```

### 2. GitHub Pages Configuration

1. Go to your repository settings on GitHub
2. Navigate to **Settings → Pages**
3. Under "Build and deployment":
   - Source: Select "GitHub Actions"
4. Your site will be available at `https://yourusername.github.io/structure_of_reality`

### 3. Update Site Configuration

Edit `_config.yml`:

```yaml
title: Structure of Reality
description: Chinese American computer scientist, navigating to the origin of intelligence.
author: Your Name
email: your-email@example.com
url: "https://yourusername.github.io"  # Update with your GitHub username
baseurl: "/structure_of_reality"
```

### 4. Facebook Integration Setup (Optional)

#### Create Facebook App and Get Page Access Token

1. Go to [Facebook Developers](https://developers.facebook.com/)
2. Create a new app (select "Business" type)
3. Add the "Facebook Login" product
4. Get a Page Access Token:
   - Go to Tools → Graph API Explorer
   - Select your app
   - Select "Get User Access Token"
   - Add permissions: `pages_manage_posts`, `pages_read_engagement`
   - Generate token
   - Use Access Token Tool to convert to long-lived token
   - Exchange for Page Access Token

5. Get your Page ID:
   - Go to your Facebook Page
   - Settings → About → Page ID

#### Configure GitHub Secrets

Add these secrets in **Settings → Secrets and variables → Actions**:

1. `FACEBOOK_PAGE_ACCESS_TOKEN` - Your page access token
2. `FACEBOOK_PAGE_ID` - Your Facebook page ID

### 5. Configure GitHub Variables

In **Settings → Secrets and variables → Actions → Variables**:

1. Add variable:
   - Name: `GITHUB_PAGES_URL`
   - Value: `https://yourusername.github.io/structure_of_reality`

*Note: This is only needed if you're using the Facebook integration.*

## ✍️ Writing Posts

### Creating a New Post

1. Create a new file in `_posts/` directory
2. Name format: `YYYY-MM-DD-title-slug.md`
3. Example: `_posts/2024-01-15-understanding-neural-networks.md`

### Post Template

```markdown
---
layout: post
title: "Your Post Title"
date: 2024-01-15 10:00:00 -0000
author: Your Name
tags: [AI, machine-learning, consciousness]
excerpt: "A brief summary of your post (appears in listings and social media)"
---

Your content here...

## Section Heading

Write your thoughts, insights, and explorations.

### Subsection

- Bullet points
- More thoughts

> Blockquotes for emphasis

\`\`\`python
# Code examples
def intelligence():
    return "understanding"
\`\`\`
```

### Front Matter Options

- `title`: Post title (required)
- `date`: Publication date and time (required)
- `author`: Author name
- `tags`: Array of tags for categorization
- `excerpt`: Short description for previews
- `canonical_url`: Original URL (auto-set to GitHub Pages URL)

## 🚀 Publishing Workflow

### Automatic Publishing

When you push a new or updated post to the `main` branch:

1. GitHub Actions detects the change
2. Jekyll builds and deploys your site to GitHub Pages
3. A link is shared on your Facebook page (if configured)
4. The post metadata is updated with Facebook post ID (if applicable)

### Manual Publishing

You can manually trigger publishing from GitHub:

1. Go to **Actions** tab in your repository
2. Select "Publish Blog Post" workflow
3. Click "Run workflow"
4. Enter the path to your post file
5. Click "Run workflow"

### Local Testing Before Publishing

```bash
# Test locally
bundle exec jekyll serve --drafts

# View at http://localhost:4000

# Publish manually to Facebook only (if configured)
cd scripts
python3 publish_to_facebook.py ../_posts/2024-01-15-my-post.md "https://yourusername.github.io/structure_of_reality/2024/01/15/my-post/"
```

## ⚙️ Configuration

### Publishing Scripts

All publishing scripts are in the `scripts/` directory:

- `publish_to_facebook.py` - Shares on Facebook
- `publish_all.sh` - Publishing helper script
- `requirements.txt` - Python dependencies

### Environment Variables

For local testing (if using Facebook integration), create a `.env` file:

```bash
export FACEBOOK_PAGE_ACCESS_TOKEN="your_token"
export FACEBOOK_PAGE_ID="your_page_id"
export GITHUB_PAGES_URL="https://yourusername.github.io/structure_of_reality"
```

Load it before running scripts:
```bash
source .env
```

### Customizing the Theme

#### Colors and Styles

Edit `assets/css/main.css` to customize:

```css
:root {
    --primary-color: #2c3e50;      /* Main color */
    --secondary-color: #3498db;     /* Accent color */
    --text-color: #333;             /* Text color */
    --light-gray: #ecf0f1;          /* Background highlights */
    --border-color: #bdc3c7;        /* Borders */
}
```

#### Layouts

Modify layouts in `_layouts/`:
- `default.html` - Base layout
- `post.html` - Blog post layout
- `page.html` - Static page layout

## 🐛 Troubleshooting

### Jekyll Build Errors

**Problem**: Bundle install fails
```bash
# Solution: Update Ruby and Bundler
gem update --system
gem install bundler
bundle install
```

**Problem**: Jekyll serve fails
```bash
# Solution: Clear cache and rebuild
bundle exec jekyll clean
bundle exec jekyll serve
```

### Publishing Errors

**Problem**: Facebook publishing fails
- Verify `FACEBOOK_PAGE_ACCESS_TOKEN` hasn't expired
- Check that your app has the required permissions
- Ensure you're using a Page Access Token, not a User Access Token

**Problem**: GitHub Actions workflow fails
- Check the Actions tab for detailed error logs
- Verify all secrets and variables are set correctly
- Ensure the post file path is correct

### Common Issues

**Problem**: Site not updating on GitHub Pages
- Wait 2-3 minutes for deployment to complete
- Check the Actions tab for build status
- Clear your browser cache

**Problem**: Images not displaying
- Ensure images are in `assets/images/` directory
- Use relative paths: `![Alt text](/assets/images/photo.jpg)`

## 📚 Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [Facebook Graph API](https://developers.facebook.com/docs/graph-api)

## 📝 Writing Tips

1. **Be Authentic**: This is your personal journal—let your voice shine through
2. **Regular Schedule**: Consistency helps build an audience
3. **Engage**: Respond to comments and engage with your readers
4. **Cross-link**: Reference previous posts to build a narrative
5. **Draft First**: Use `_drafts/` folder for works in progress

## 🤝 Contributing

This is a personal blog, but if you find issues with the setup or have suggestions:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

All blog content is © Tim. All rights reserved.

The technical framework and automation code are provided for reference. 
If you wish to use them for your own blog, please remove all original content 
and provide attribution.

---

## 🚀 Next Steps

1. ✅ Set up your GitHub repository
2. ✅ Configure GitHub Pages
3. ✅ Set up Facebook integration (optional)
4. ✅ Write your first post
5. ✅ Push to GitHub and watch it deploy!

**Happy writing! May your exploration of intelligence and reality be fruitful.**

