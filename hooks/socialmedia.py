"""
MkDocs hook to add LinkedIn share buttons to blog posts.

This hook adds a LinkedIn share button to blog posts, allowing readers
to easily share content on LinkedIn with pre-filled title and URL.
"""

import logging
from urllib.parse import quote

from mkdocs.plugins import get_plugin_logger

log = get_plugin_logger(__name__)


def on_page_content(html, page, config, files):
    """
    Add LinkedIn share button to blog posts.

    This hook injects a LinkedIn share button at the end of blog post content.
    The button includes the post title and URL for easy sharing.

    Args:
        html: The rendered HTML content of the page
        page: The page object being processed
        config: The MkDocs configuration
        files: All files in the documentation

    Returns:
        Modified HTML with LinkedIn share button
    """
    # Only add share button to blog posts (not the index or tags pages)
    if page.file.src_uri.startswith("posts/"):

        # Get the full URL of the page
        site_url = config.get("site_url", "").rstrip("/")
        page_url = f"{site_url}/{page.url.lstrip('/')}" if site_url else page.url

        # Get the page title and description
        page_title = page.title or "Check out this post"
        page_description = ""
        if hasattr(page, "meta") and page.meta:
            page_description = page.meta.get("description", "")
        if not page_description:
            page_description = config.get("site_description", "")

        # URL encode the page URL for LinkedIn
        encoded_url = quote(page_url, safe="")

        # Create LinkedIn share URL with both URL and summary text
        # Format: https://www.linkedin.com/sharing/share-offsite/?url=ENCODED_URL
        # LinkedIn will fetch title/description from Open Graph tags if the URL is accessible
        # For local testing or when OG tags aren't accessible, the title shows in the browser
        linkedin_share_url = (
            f"https://www.linkedin.com/sharing/share-offsite/?url={encoded_url}"
        )

        # Create the share button HTML with styling
        share_button_html = f"""
<div class="social-share-container" style="margin-top: 2rem; padding: 1.5rem; border-top: 2px solid var(--md-default-fg-color--lightest); text-align: center;">
    <p style="margin-bottom: 1rem; color: var(--md-default-fg-color--light); font-size: 0.9rem;">
        <strong>Found this helpful? Share it on LinkedIn!</strong>
    </p>
    <a href="{linkedin_share_url}" 
       target="_blank" 
       rel="noopener noreferrer"
       class="linkedin-share-button"
       style="display: inline-flex; align-items: center; gap: 0.5rem; padding: 0.75rem 1.5rem; 
              background-color: #0A66C2; color: white; text-decoration: none; 
              border-radius: 4px; font-weight: 500; transition: background-color 0.3s ease;
              box-shadow: 0 2px 4px rgba(0,0,0,0.1);"
       onmouseover="this.style.backgroundColor='#004182'"
       onmouseout="this.style.backgroundColor='#0A66C2'">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
            <path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/>
        </svg>
        Share on LinkedIn
    </a>
</div>

<style>
    .linkedin-share-button:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }}
    
    @media (max-width: 768px) {{
        .social-share-container {{
            padding: 1rem;
        }}
        .linkedin-share-button {{
            width: 100%;
            justify-content: center;
        }}
    }}
</style>
"""

        # Inject the share button before the closing body content
        html = html + share_button_html

        log.info(f"Added LinkedIn share button to: {page.file.src_uri}")

    return html


def on_post_page(output, page, config):
    """
    Optional: Add Open Graph meta tags for better LinkedIn preview.

    This ensures that when posts are shared on LinkedIn, they display
    with proper title, description, and image preview.

    Args:
        output: The complete HTML output
        page: The page object
        config: The MkDocs configuration

    Returns:
        Modified HTML output with Open Graph tags
    """
    # Only add meta tags to blog posts
    if page.file.src_uri.startswith("posts/"):
        site_url = config.get("site_url", "").rstrip("/")
        page_url = f"{site_url}/{page.url}" if site_url else page.url
        page_title = page.title or config.get("site_name", "Blog Post")
        page_description = config.get("site_description", "")

        # Extract description from page meta if available
        if hasattr(page, "meta") and page.meta:
            page_description = page.meta.get("description", page_description)

        # Create Open Graph meta tags
        og_tags = f"""
    <!-- Open Graph / LinkedIn meta tags -->
    <meta property="og:type" content="article" />
    <meta property="og:url" content="{page_url}" />
    <meta property="og:title" content="{page_title}" />
    <meta property="og:description" content="{page_description}" />
    <meta property="og:site_name" content="{config.get('site_name', '')}" />
    
    <!-- Twitter Card meta tags (also used by LinkedIn) -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{page_title}" />
    <meta name="twitter:description" content="{page_description}" />
"""

        # Insert meta tags in the <head> section
        if "<head>" in output:
            output = output.replace("<head>", f"<head>{og_tags}", 1)
            log.info(f"Added Open Graph meta tags to: {page.file.src_uri}")

    return output
