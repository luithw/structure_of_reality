# Contributing to Structure of Reality

Thank you for your interest in contributing to the Structure of Reality blog framework!

While this is primarily a personal blog, contributions to improve the blog infrastructure, automation scripts, and documentation are welcome.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the GitHub Issues
2. If not, create a new issue with:
   - Clear description of the problem or suggestion
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Your environment (OS, Ruby version, etc.)

### Submitting Changes

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/structure_of_reality.git
   cd structure_of_reality
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Update documentation if needed
   - Test your changes locally

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your feature branch
   - Describe your changes

## Areas for Contribution

### Welcome Contributions

- Bug fixes in automation scripts
- Improvements to GitHub Actions workflows
- Documentation enhancements
- CSS/design improvements
- Additional publishing integrations (e.g., LinkedIn, Twitter/X)
- SEO optimizations
- Accessibility improvements
- Mobile responsiveness enhancements

### Not Accepting

- Blog content (this is a personal blog)
- Major theme overhauls without discussion
- Changes that break backward compatibility

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8
- Use meaningful variable names
- Add docstrings to functions
- Handle errors gracefully

**CSS:**
- Use CSS variables for colors and spacing
- Maintain mobile-first responsive design
- Keep styles organized by component

**Jekyll/HTML:**
- Use semantic HTML
- Keep layouts DRY (Don't Repeat Yourself)
- Maintain accessibility standards

### Testing

Before submitting:

1. **Test locally**
   ```bash
   bundle exec jekyll serve
   ```

2. **Test publishing scripts** (if applicable)
   ```bash
   cd scripts
   python3 publish_to_facebook.py ../path/to/test-post.md "https://example.com/post-url"
   ```

3. **Check for errors**
   - No Jekyll build errors
   - No Python syntax errors
   - No broken links

### Documentation

- Update README.md if you change functionality
- Add comments to complex code
- Update setup instructions if needed

## Pull Request Process

1. Ensure your PR description clearly describes the problem and solution
2. Link any related issues
3. Ensure all tests pass
4. Update documentation as needed
5. Be responsive to feedback

## Questions?

If you have questions about contributing, feel free to:
- Open an issue for discussion
- Check existing documentation
- Review closed PRs for examples

## Code of Conduct

### Our Standards

- Be respectful and inclusive
- Provide constructive feedback
- Focus on what is best for the project
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Personal or political attacks
- Publishing others' private information

## License

By contributing to the technical framework (scripts, workflows, templates), you agree 
that your contributions may be used by others who adapt this framework for their own blogs. 
However, all blog content remains the exclusive copyright of the original author.

---

Thank you for helping improve the Structure of Reality blog framework! 🚀

