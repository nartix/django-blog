from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages
from django.shortcuts import redirect
import bleach


def encode_base64_key(id):
    return urlsafe_base64_encode(force_bytes(id))


def decode_base64_key(id):
    return force_str(urlsafe_base64_decode(id))


def sanitize_html(content):
    # List of allowed HTML tags based on Tiptap usage and additional common elements
    allowed_tags = [
        'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'pre', 'code',
        'ul', 'ol', 'li', 'strong', 'em', 'a', 'img', 'div', 'span',
        'br', 'hr', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'td', 'th',
    ]

    # Allowed attributes for the corresponding tags
    allowed_attrs = {
        'a': ['href', 'title', 'target', 'rel'],
        'img': ['src', 'alt', 'title', 'width', 'height'],
        'div': ['class'],
        'span': ['class'],
        'p': ['class'],
        'code': ['class'],
        # Add other attributes as needed for your application
    }

    # Clean the content
    sanitized_content = bleach.clean(
        content, tags=allowed_tags, attributes=allowed_attrs, strip=True)

    return sanitized_content


def redirect_with_message(request, message_type, message, redirect_url):
    if message_type == 'error':
        messages.error(request, message)
    elif message_type == 'success':
        messages.success(request, message)
    elif message_type == 'info':
        messages.info(request, message)
    elif message_type == 'warning':
        messages.warning(request, message)
    elif message_type == 'debug':
        messages.debug(request, message)
    else:
        raise ValueError(f"Invalid message type: {message_type}")
    return redirect(redirect_url)
