# Structure of Reality

**Chinese American computer scientist, navigating to the origin of intelligence.**

A personal blog series and research journal exploring artificial intelligence, consciousness, spatial intelligence, and the fundamental nature of reality. This site is hosted with Jekyll and GitHub Pages and serves as the writing layer around the broader research program.

## 🌟 Features

- **Static Site Generator**: Built with Jekyll for a fast, simple, and maintainable blog
- **GitHub Pages Hosting**: Free hosting with straightforward deployment
- **Personal Research Journal**: A home for long-form writing on intelligence, consciousness, and AI research
- **Modern Design**: Clean responsive layout optimized for reading
- **Post Archive**: Dedicated archive page for browsing the essay series
- **Notification Scripts**: Optional scripts for email and SMS notifications
- **SEO Friendly**: Metadata and shareable post pages via Jekyll layouts

## 📋 Repository Structure

This repository currently contains:

```text
structure-of-reality/
  CONTRIBUTING.md
  FEATURES.md
  Gemfile
  LICENSE
  NEXT_STEPS.md
  QUICKSTART.md
  README.md
  SETUP_CHECKLIST.md
  _config.yml
  _layouts/
    default.html
    page.html
    post.html
  _posts/
    2024-01-01-welcome-to-structure-of-reality.md
    2026-01-11-the-spatial-hypothesis-of-intelligence.md
    2026-01-11-what-is-structure-of-reality.md
  about.md
  archive.html
  assets/
    css/
      main.css
  index.html
  scripts/
    publish_all.sh
    requirements.txt
    send_email_notification.py
    send_sms_notification.py
```

## 📚 Documentation Files

- `QUICKSTART.md` — quick setup and first-run guidance
- `FEATURES.md` — overview of site capabilities
- `SETUP_CHECKLIST.md` — practical setup checklist
- `NEXT_STEPS.md` — suggested follow-up tasks for growing the blog
- `CONTRIBUTING.md` — contribution guidance

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
   git clone https://github.com/luithw/structure_of_reality.git
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

## 🔧 Site Structure

### Core Pages

- `index.html` — homepage
- `about.md` — about page
- `archive.html` — archive of posts

### Layouts

Layouts live in `_layouts/`:
- `default.html` — base layout
- `post.html` — post layout
- `page.html` — static page layout

### Styling

- `assets/css/main.css` — site styling

### Configuration

- `_config.yml` — Jekyll site configuration
- `Gemfile` — Ruby dependencies for local development

## ✍️ Writing Posts

### Creating a New Post

1. Create a new file in `_posts/`
2. Use the format `YYYY-MM-DD-title-slug.md`
3. Example:
   ```text
   _posts/2026-03-15-far-arena-a-transport-test-for-artificial-spatial-intelligence.md
   ```

### Post Template

```markdown
---
layout: post
title: "Your Post Title"
date: 2026-03-15 10:00:00 -0000
author: Tim Lui
tags: [AI, spatial-intelligence, consciousness]
excerpt: "A brief summary of your post"
---

Your content here...
```

### Current Posts

Current published posts in `_posts/`:

1. `2024-01-01-welcome-to-structure-of-reality.md`
2. `2026-01-11-what-is-structure-of-reality.md`
3. `2026-01-11-the-spatial-hypothesis-of-intelligence.md`
4. `2026-03-15-far-arena-a-transport-test-for-artificial-spatial-intelligence.md` — new FAR essay connecting the blog to the Forage-Avoid-Return research program

## 🧠 Research Series Direction

This project is the writing and reflection layer for a broader research agenda on intelligence. Current themes include:

- What is Structure of Reality?
- The Spatial Hypothesis of Intelligence
- Artificial Spatial Intelligence
- Spatial Temporal Reasoning
- Forage, Avoid, Return
- The automation of science
- Consciousness and the architecture of mind

## 🆕 New Post in the Series

### FAR Arena: A Transport Test for Artificial Spatial Intelligence

This new post introduces the **Forage-Avoid-Return (FAR) Arena**, a benchmark for testing whether an artificial agent can rapidly acquire a usable internal map in a novel environment.

Core ideas include:
- sparse geometric sensing instead of texture-heavy vision
- survival as a cyclic problem of forage, avoid, and return
- transport or drop-in evaluation on novel maps
- comparison between single-tier recurrent agents and two-tier hippocampus-cortex-like architectures
- using the benchmark as a substrate for automated scientific iteration on agent design

This post helps connect the philosophical direction of *Structure of Reality* to the concrete research program in *Artificial Spatial Intelligence*.

## 🚀 Publishing Workflow

### Local Build

```bash
bundle exec jekyll serve
```

### Publish via Git

Commit changes and push to the main branch of the GitHub repository.

```bash
git add .
git commit -m "Add new blog post"
git push origin main
```

### Optional Scripts

The `scripts/` directory currently contains:

- `publish_all.sh`
- `send_email_notification.py`
- `send_sms_notification.py`
- `requirements.txt`

If you use these scripts, install Python dependencies first:

```bash
cd scripts
pip install -r requirements.txt
```

## ⚙️ Configuration

Update `_config.yml` with your site details:

```yaml
title: Structure of Reality
description: Chinese American computer scientist, navigating to the origin of intelligence.
author: Tim Lui
email: lui.thw@gmail.com
url: "https://luithw.github.io"
baseurl: "/structure_of_reality"
```

## 🐛 Troubleshooting

### Jekyll Build Errors

**Problem**: `bundle install` fails
```bash
gem update --system
gem install bundler
bundle install
```

**Problem**: `jekyll serve` fails
```bash
bundle exec jekyll clean
bundle exec jekyll serve
```

### Common Issues

**Problem**: Site not updating on GitHub Pages
- Wait a few minutes for deployment
- Check GitHub Pages settings
- Clear browser cache

**Problem**: Styles not loading correctly
- Confirm `assets/css/main.css` exists
- Verify `_config.yml` `baseurl` is correct

## 📚 Resources

- [Jekyll Documentation](https://jekyllrb.com/docs/)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)

## 📝 Writing Tips

1. **Be Authentic**: This is your personal journal and research voice
2. **Think in Series**: Let posts connect to one another as a long arc
3. **Bridge Philosophy and Engineering**: Use the blog to connect deep ideas to concrete experiments
4. **Cross-link Posts**: Build a narrative across essays
5. **Draft Iteratively**: Start rough, then compress into clarity

## 🤝 Contributing

This is a personal blog, but suggestions on structure, tooling, or publishing workflow are welcome.

## 📄 License

All blog content is © Tim. All rights reserved.

The technical framework and automation code are provided for reference. If you reuse them, remove original content and provide attribution.

---

## 🚀 Next Steps

1. Add the FAR post to `_posts/`
2. Cross-link FAR with `what-is-structure-of-reality` and `the-spatial-hypothesis-of-intelligence`
3. Expand the archive page as the essay series grows
4. Refine the site theme and metadata
5. Continue publishing the research journey

**Happy writing. May the structure reveal itself through sustained inquiry.**