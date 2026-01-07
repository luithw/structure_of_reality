# Quick Start Guide

Get your "Structure of Reality" blog up and running in minutes!

## Step 1: Initial Setup (5 minutes)

```bash
# Navigate to your project directory
cd /home/tim/code/structure_of_reality

# Install Jekyll dependencies
bundle install

# Test locally
bundle exec jekyll serve
```

Visit `http://localhost:4000` to see your blog!

## Step 2: Customize Your Blog (10 minutes)

Edit `_config.yml`:

```yaml
title: Structure of Reality
author: Tim Lui
email: lui.thw@gmail.com
url: "https://luithw.github.io"
baseurl: "/structure_of_reality"
```

## Step 3: Create GitHub Repository (5 minutes)

```bash
# Initialize git (if not already done)
git init
git add .
git commit -m "Initial commit: Structure of Reality blog"

# Create repository on GitHub, then:
git remote add origin https://github.com/luithw/structure_of_reality.git
git branch -M main
git push -u origin main
```

## Step 4: Enable GitHub Pages (2 minutes)

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Build and deployment", select **GitHub Actions**
4. Done! Your site will be live in a few minutes

## Step 5: Set Up Facebook (10 minutes) - Optional

### Get Facebook Page Access Token

1. Go to https://developers.facebook.com/
2. Create an app (type: Business)
3. Add "Facebook Login" product
4. Go to **Tools** → **Graph API Explorer**
5. Select your app, get user token with permissions:
   - `pages_manage_posts`
   - `pages_read_engagement`
6. Use the Access Token Tool to get a long-lived token
7. Exchange for Page Access Token

### Get Page ID

1. Go to your Facebook Page
2. **Settings** → **About** → Page ID

### Add to GitHub

In **Settings** → **Secrets and variables** → **Actions**:
1. Add secret `FACEBOOK_PAGE_ACCESS_TOKEN`
2. Add secret `FACEBOOK_PAGE_ID`

## Step 6: Configure Publishing URL (1 minute) - Only if using Facebook

In GitHub: **Settings** → **Secrets and variables** → **Actions** → **Variables** tab:
- Name: `PAGES_URL`
- Value: `https://luithw.github.io/structure_of_reality`

## Step 7: Write Your First Post! (∞ minutes)

Create `_posts/2024-01-06-my-first-post.md`:

```markdown
---
layout: post
title: "My First Exploration"
date: 2024-01-06 10:00:00 -0000
tags: [AI, intelligence, philosophy]
excerpt: "Beginning my journey into understanding intelligence..."
---

Your thoughts here...
```

## Step 8: Publish Everything

```bash
git add _posts/2024-01-06-my-first-post.md
git commit -m "Add first post"
git push
```

**That's it!** GitHub Actions will automatically:
- Deploy to GitHub Pages
- Share on Facebook (if configured)

## Verification Checklist

After pushing:
1. ✅ Check GitHub Actions tab (should see green checkmarks)
2. ✅ Visit your GitHub Pages URL (wait 2-3 minutes)
3. ✅ Check Facebook page (if configured)

## Writing Your Next Post

```bash
# Create new post file
code _posts/2024-01-07-second-post.md

# Write your content

# Publish
git add _posts/2024-01-07-second-post.md
git commit -m "Add post: Second post title"
git push
```

## Local Publishing (Optional)

For testing or manual publishing:

```bash
cd scripts

# Create Python virtual environment (first time only)
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables (if using Facebook)
export FACEBOOK_PAGE_ACCESS_TOKEN="your_token"
export FACEBOOK_PAGE_ID="your_page_id"
export GITHUB_PAGES_URL="https://luithw.github.io/structure_of_reality"  # Note: for GitHub Actions, use PAGES_URL variable

# Publish to Facebook
python3 publish_to_facebook.py ../_posts/2024-01-06-my-first-post.md "https://luithw.github.io/structure_of_reality/2024/01/06/my-first-post/"
```

## Troubleshooting

**Site not building?**
- Check GitHub Actions logs for errors
- Verify `_config.yml` syntax

**Facebook not working?**
- Verify secrets are set correctly
- Check token hasn't expired

**Local Jekyll errors?**
```bash
bundle update
bundle exec jekyll clean
bundle exec jekyll serve
```

## Next Steps

- [ ] Read the full [README.md](README.md) for detailed documentation
- [ ] Follow the [SETUP_CHECKLIST.md](SETUP_CHECKLIST.md)
- [ ] Customize the CSS in `assets/css/main.css`
- [ ] Update the About page
- [ ] Start writing regularly!

---

**You're all set!** Begin your journey navigating to the origin of intelligence. 🚀

