# Setup Checklist

Use this checklist to track your progress in setting up the Structure of Reality blog.

## Initial Setup

- [ ] Clone or create the repository locally
- [ ] Install Ruby and Bundler
- [ ] Run `bundle install` to install Jekyll dependencies
- [ ] Test locally with `bundle exec jekyll serve`
- [ ] Verify site works at `http://localhost:4000`

## GitHub Configuration

- [ ] Create GitHub repository named `structure_of_reality`
- [ ] Push code to GitHub
- [ ] Enable GitHub Pages in repository settings
- [ ] Select "GitHub Actions" as the source
- [ ] Verify site is accessible at your GitHub Pages URL

## Site Customization

- [ ] Update `_config.yml` with your information:
  - [ ] Update `author` field
  - [ ] Update `email` field
  - [ ] Update `url` with your GitHub username
  - [ ] Review and adjust `baseurl` if needed
- [ ] Customize `about.md` page
- [ ] Review and adjust colors in `assets/css/main.css` (optional)

## Facebook Integration (Optional)

- [ ] Create Facebook Page (if you don't have one)
- [ ] Go to [Facebook Developers](https://developers.facebook.com/)
- [ ] Create a new app
- [ ] Add Facebook Login product
- [ ] Generate Page Access Token with required permissions:
  - [ ] `pages_manage_posts`
  - [ ] `pages_read_engagement`
- [ ] Convert to long-lived token
- [ ] Get your Facebook Page ID
- [ ] Add credentials to GitHub repository secrets:
  - [ ] Add `FACEBOOK_PAGE_ACCESS_TOKEN` secret
  - [ ] Add `FACEBOOK_PAGE_ID` secret

## GitHub Actions Configuration

- [ ] Add GitHub Actions variable:
  - [ ] Go to Settings → Secrets and variables → Actions → Variables
  - [ ] Add `GITHUB_PAGES_URL` variable with your full GitHub Pages URL
- [ ] Verify GitHub Actions workflows are present:
  - [ ] `.github/workflows/jekyll.yml` (for site deployment)
  - [ ] `.github/workflows/publish.yml` (for cross-posting)
- [ ] Check that workflows have necessary permissions

## Testing

- [ ] Write a test post in `_posts/` directory
- [ ] Commit and push to GitHub
- [ ] Verify GitHub Actions workflows run successfully
- [ ] Check that site is updated on GitHub Pages
- [ ] Verify post is shared on Facebook (if configured)
- [ ] Check that post metadata is updated with Facebook post ID (if applicable)

## Local Publishing Setup (Optional)

- [ ] Install Python 3.8+ on your local machine
- [ ] Navigate to `scripts/` directory
- [ ] Create virtual environment: `python3 -m venv venv`
- [ ] Activate virtual environment: `source venv/bin/activate`
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Create `.env` file with your credentials
- [ ] Test local publishing scripts

## Final Checks

- [ ] Remove or update the sample post
- [ ] Write your first real post
- [ ] Test all social sharing buttons
- [ ] Check responsive design on mobile
- [ ] Verify RSS feed is working
- [ ] Set up Google Analytics (optional)
- [ ] Submit sitemap to search engines (optional)

## Maintenance Tasks

- [ ] Set up a regular posting schedule
- [ ] Monitor GitHub Actions for any failures
- [ ] Check Facebook analytics (if using)
- [ ] Update dependencies periodically:
  - [ ] Run `bundle update` for Ruby gems
  - [ ] Run `pip install --upgrade -r requirements.txt` for Python packages
- [ ] Backup your content regularly

## Troubleshooting Resources

If you encounter issues, check:
- [ ] GitHub Actions logs in the Actions tab
- [ ] Jekyll build errors in terminal
- [ ] API response errors in workflow logs
- [ ] README.md troubleshooting section

---

## Notes

Use this space to track any specific issues or customizations:

```
[Write your notes here]
```

---

**Once everything is checked off, you're ready to start your journey!**

🚀 Happy blogging and may your exploration of intelligence and reality be profound!

