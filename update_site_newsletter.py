#!/usr/bin/env python3
"""Update all HTML files in _site with the new newsletter code."""

import os
import re
from pathlib import Path

# The old Buttondown form pattern
old_pattern = r'''            <div class="newsletter-section">
                <h3>📬 Subscribe to Newsletter</h3>
                <p>Get notified when I publish new articles\. No spam, unsubscribe anytime\.</p>
                <form class="newsletter-form" action="https://buttondown\.email/api/emails/embed-subscribe/[^"]*" method="post" target="popupwindow" onsubmit="window\.open\('https://buttondown\.email/[^']*', 'popupwindow'\)">
                    <input type="email" name="email" placeholder="Enter your email" required>
                    <button type="submit">Subscribe</button>
                </form>
                <p class="newsletter-note">Powered by <a href="https://buttondown\.email" target="_blank">Buttondown</a></p>
            </div>'''

# The new custom API form
new_form = '''            <div class="newsletter-section">
                <h3>📬 Subscribe to Newsletter</h3>
                <p>Get notified when I publish new articles. No spam, unsubscribe anytime.</p>
                <form class="newsletter-form" id="newsletter-form">
                    <input type="email" id="newsletter-email" name="email" placeholder="Enter your email" required>
                    <button type="submit">Subscribe</button>
                </form>
                <div id="newsletter-message" style="display: none; margin-top: 10px; padding: 10px; border-radius: 4px;"></div>
</div>

            <script>
            (function() {
                const form = document.getElementById('newsletter-form');
                const emailInput = document.getElementById('newsletter-email');
                const messageEl = document.getElementById('newsletter-message');
                
                if (!form) return;
                
                form.addEventListener('submit', function(e) {
                    e.preventDefault();
                    
                    const email = emailInput.value.trim();
                    if (!email) {
                        showMessage('Please enter an email address', 'error');
                        return;
                    }
                    
                    // Calculate API base URL from current page path
                    const pathParts = window.location.pathname.split('/').filter(p => p);
                    let apiBase = '';
                    
                    // If we're in a subpath (e.g., /u/tim-lui/p/...), go up to root
                    if (pathParts.length > 0 && pathParts[0] === 'u') {
                        apiBase = '/';
                    } else {
                        apiBase = '/';
                    }
                    
                    const button = form.querySelector('button');
                    button.disabled = true;
                    button.textContent = 'Subscribing...';
                    
                    fetch(apiBase + '/api/newsletter/subscribe', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email: email })
                    })
                        .then(r => r.json())
                        .then(data => {
                            if (data.error) {
                                showMessage(data.error, 'error');
                            } else {
                                showMessage('✅ ' + data.message, 'success');
                                emailInput.value = '';
                            }
                            button.disabled = false;
                            button.textContent = 'Subscribe';
                        })
                        .catch(err => {
                            console.error('Error subscribing:', err);
                            showMessage('Something went wrong. Please try again.', 'error');
                            button.disabled = false;
                            button.textContent = 'Subscribe';
                        });
                });
                
                function showMessage(text, type) {
                    messageEl.textContent = text;
                    messageEl.className = 'newsletter-' + type;
                    messageEl.style.display = 'block';
                    
                    if (type === 'success') {
                        setTimeout(() => {
                            messageEl.style.display = 'none';
                        }, 5000);
                    }
                }
            })();
            </script>'''

# Find all HTML files in _site
site_dir = Path('_site')
html_files = list(site_dir.rglob('*.html'))

print(f"Found {len(html_files)} HTML files in _site/")

updated_count = 0
for html_file in html_files:
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Try to replace the newsletter section
        new_content = re.sub(old_pattern, new_form, content, flags=re.MULTILINE)
        
        if new_content != content:
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1
            print(f"✅ Updated {html_file.relative_to(site_dir)}")
    except Exception as e:
        print(f"⚠️  Error processing {html_file}: {e}")

print(f"\n✅ Updated {updated_count} files")
