import os
import re

base_path = r"d:\first_project\sanjeri_perfume\sanjeri_project\-ecommerce_project\core\settings\base.py"
with open(base_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update INSTALLED_APPS
apps_additions = """
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'sslserver', 
    'mathfilters',
]"""
content = content.replace("]\n", apps_additions, 1) if "'allauth'" not in content else content

# 2. Update TEMPLATES
context_processors_additions = """
                'apps.context_processors.cart_and_wishlist_context',
                'apps.context_processors.wallet_balance',
                'apps.context_processors.offer_context',
            ],"""
if "'apps.context_processors.cart_and_wishlist_context'" not in content:
    content = content.replace("            ],", context_processors_additions, 1)

# 3. Add API Keys & Allauth config at bottom
additions = """

# Razorpay Configuration
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

# Email configuration
RESEND_API_KEY = os.getenv('RESEND_API_KEY')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'support@sanjeriperfume.in')

# Authentication backends
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# Allauth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGOUT_ON_GET = True
SOCIALACCOUNT_LOGIN_ON_GET = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_STORE_TOKENS = True

SOCIALACCOUNT_ADAPTER = 'apps.adapters.CustomSocialAccountAdapter'

LOGIN_REDIRECT_URL = 'homepage'
LOGOUT_REDIRECT_URL = 'user_login'
LOGIN_URL = '/user_login/'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': ['profile', 'email'],
        'AUTH_PARAMS': {'access_type': 'online'},
        'APP': {
            'client_id': os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY'),
            'secret': os.getenv('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', ''),
            'key': ''
        }
    }
}
"""

if "RAZORPAY_KEY_ID" not in content:
    content += additions

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("base.py updated successfully!")
