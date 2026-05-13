#!/usr/bin/env python3
"""Update default.html to use custom newsletter API instead of Buttondown."""

import re

# Read the file
with open('_layouts/default.html', 'r') as f:
    content = f.read()

# Find and replace the newsletter section
old_newsletter = r'''            <div class="newsletter-section">
                <h3>📬 Subscribe to Newsletter</h3>
                <p>Get notified when I publish new articles\. No spam, unsubscribe anytime\.</p>
                <form class="newsletter-form" action="https://buttondown\.email/api/emails/embed-subscribe/\{\{ site\.buttondown_username \| default: 'structureofreality' \}\}" method="post" target="popupwindow" onsubmit="window\.open\('https://buttondown\.email/\{\{ site\.buttondown_username \| default: 'structureofreality' \}\}', 'popupwindow'\)">
                    <input type="email" name="email" placeholder="Enter your email" required>
                    <button type="submit">Subscribe</button>
                </form>
                <p class="newsletter-note">Powered by <a href="https://buttondown\.email" target="_blank">Buttondown</a></p>
            </div>'''

new_newsletter = '''            <div class="newsletter-section">
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

# Replace using regex
content = re.sub(old_newsletter, new_newsletter, content, flags=re.MULTILINE)

# Write back
with open('_layouts/default.html', 'w') as f:
    f.write(content)

print("✅ Updated default.html with custom newsletter API")
