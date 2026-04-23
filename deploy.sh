#!/bin/bash
# =============================================================
# Sanjeri Perfumes - Full Deployment Script
# Server: 209.38.123.149 | Ubuntu 24.04
# Run as root: bash deploy.sh
# =============================================================

set -e  # Exit on any error

# ── Colors ────────────────────────────────────────────────────
RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; NC='\033[0m'
info()    { echo -e "${GREEN}[INFO]${NC} $1"; }
warning() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ── Config ────────────────────────────────────────────────────
PROJECT_DIR="/var/www/sanjeri"
REPO_URL="https://github.com/AncyFaisal/ecommerce_project_host.git"
DOMAIN="sanjeriperfume.in"
WWW_DOMAIN="www.sanjeriperfume.in"
SERVER_IP="209.38.123.149"
DB_NAME="sanjeri_db"
DB_USER="sanjeri_user"
PYTHON="python3"
VENV="$PROJECT_DIR/venv"

# ── Generate secrets ──────────────────────────────────────────
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
DB_PASSWORD=$(python3 -c "import secrets; print(secrets.token_hex(16))")

info "============================================"
info " Sanjeri Perfumes Deployment Starting"
info "============================================"

# ── Step 1: System update ─────────────────────────────────────
info "Step 1/12: Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq

# ── Step 2: Install dependencies ──────────────────────────────
info "Step 2/12: Installing system dependencies..."
apt-get install -y -qq \
    python3 python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib \
    nginx certbot python3-certbot-nginx \
    git curl build-essential libpq-dev \
    supervisor

# ── Step 3: PostgreSQL setup ──────────────────────────────────
info "Step 3/12: Setting up PostgreSQL database..."
systemctl start postgresql
systemctl enable postgresql

sudo -u postgres psql <<EOF
DO \$\$
BEGIN
  IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '$DB_USER') THEN
    CREATE USER $DB_USER WITH PASSWORD '$DB_PASSWORD';
  END IF;
END
\$\$;
EOF

sudo -u postgres psql -c "ALTER USER $DB_USER WITH PASSWORD '$DB_PASSWORD';"
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME OWNER $DB_USER;" 2>/dev/null || \
    sudo -u postgres psql -c "ALTER DATABASE $DB_NAME OWNER TO $DB_USER;"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'Asia/Kolkata';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

info "  DB_NAME=$DB_NAME  DB_USER=$DB_USER  DB_PASSWORD=$DB_PASSWORD"

# ── Step 4: Clone / update project ───────────────────────────
info "Step 4/12: Cloning project from GitHub..."
if [ -d "$PROJECT_DIR/.git" ]; then
    info "  Repo exists — pulling latest..."
    cd "$PROJECT_DIR"
    git pull origin main
else
    git clone "$REPO_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

# ── Step 5: Virtual environment ───────────────────────────────
info "Step 5/12: Setting up Python virtual environment..."
$PYTHON -m venv "$VENV"
source "$VENV/bin/activate"
pip install --upgrade pip -q
pip install -r requirements.txt -q
pip install gunicorn -q

# ── Step 6: Create .env file ──────────────────────────────────
info "Step 6/12: Creating .env file..."
cat > "$PROJECT_DIR/.env" <<ENVFILE
DEBUG=False
DJANGO_SECRET_KEY=$SECRET_KEY
DJANGO_ALLOWED_HOSTS=$SERVER_IP,$DOMAIN,$WWW_DOMAIN
DJANGO_SETTINGS_MODULE=core.settings.production

DB_NAME=$DB_NAME
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_HOST=localhost
DB_PORT=5432

RESEND_API_KEY=YOUR_RESEND_API_KEY
DEFAULT_FROM_EMAIL=support@sanjeriperfume.in

RAZORPAY_KEY_ID=YOUR_RAZORPAY_KEY_ID
RAZORPAY_KEY_SECRET=YOUR_RAZORPAY_KEY_SECRET

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=YOUR_GOOGLE_CLIENT_ID
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=YOUR_GOOGLE_CLIENT_SECRET
ENVFILE

chmod 600 "$PROJECT_DIR/.env"

# ── Step 7: Django setup ──────────────────────────────────────
info "Step 7/12: Running Django migrations and collectstatic..."
cd "$PROJECT_DIR"
source "$VENV/bin/activate"
export DJANGO_SETTINGS_MODULE=core.settings.production

mkdir -p /var/log/sanjeri
mkdir -p "$PROJECT_DIR/media"

python manage.py migrate --noinput
python manage.py collectstatic --noinput

# ── Step 8: Gunicorn systemd service ─────────────────────────
info "Step 8/12: Creating Gunicorn service..."
cat > /etc/systemd/system/sanjeri.service <<SERVICE
[Unit]
Description=Sanjeri Gunicorn Daemon
After=network.target postgresql.service

[Service]
User=root
Group=www-data
WorkingDirectory=$PROJECT_DIR
EnvironmentFile=$PROJECT_DIR/.env
ExecStart=$VENV/bin/gunicorn \\
    --access-logfile /var/log/sanjeri/access.log \\
    --error-logfile /var/log/sanjeri/error.log \\
    --workers 3 \\
    --timeout 120 \\
    --bind unix:/run/sanjeri.sock \\
    core.wsgi:application
Restart=on-failure
RestartSec=5s

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload
systemctl start sanjeri
systemctl enable sanjeri

# Wait for socket
sleep 3
if systemctl is-active --quiet sanjeri; then
    info "  Gunicorn started successfully"
else
    error "  Gunicorn failed to start. Check: journalctl -u sanjeri -n 50"
fi

# ── Step 9: Nginx config ──────────────────────────────────────
info "Step 9/12: Configuring Nginx..."

# Remove default site
rm -f /etc/nginx/sites-enabled/default

cat > /etc/nginx/sites-available/sanjeri <<NGINX
server {
    listen 80;
    server_name $DOMAIN $WWW_DOMAIN $SERVER_IP;

    client_max_body_size 20M;

    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }

    location /static/ {
        alias $PROJECT_DIR/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location /media/ {
        alias $PROJECT_DIR/media/;
        expires 7d;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/sanjeri.sock;
        proxy_read_timeout 120;
        proxy_connect_timeout 120;
    }

    access_log /var/log/nginx/sanjeri_access.log;
    error_log  /var/log/nginx/sanjeri_error.log;
}
NGINX

ln -sf /etc/nginx/sites-available/sanjeri /etc/nginx/sites-enabled/sanjeri

nginx -t && systemctl restart nginx && systemctl enable nginx
info "  Nginx configured and restarted"

# ── Step 10: Firewall ─────────────────────────────────────────
info "Step 10/12: Configuring firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# ── Step 11: SSL certificate ──────────────────────────────────
info "Step 11/12: Attempting SSL certificate (requires DNS to be pointed)..."
if host "$DOMAIN" 2>/dev/null | grep -q "$SERVER_IP"; then
    certbot --nginx -d "$DOMAIN" -d "$WWW_DOMAIN" \
        --non-interactive --agree-tos --email "support@sanjeriperfume.in" \
        --redirect
    info "  SSL certificate installed!"
else
    warning "  DNS not yet pointing to this server."
    warning "  After pointing GoDaddy DNS, run:"
    warning "  certbot --nginx -d $DOMAIN -d $WWW_DOMAIN --non-interactive --agree-tos --email support@sanjeriperfume.in --redirect"
fi

# ── Step 12: Auto-renew SSL ───────────────────────────────────
info "Step 12/12: Setting up SSL auto-renewal..."
(crontab -l 2>/dev/null; echo "0 12 * * * /usr/bin/certbot renew --quiet") | crontab -

# ── Summary ───────────────────────────────────────────────────
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN} DEPLOYMENT COMPLETE!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "  Site URL  : http://$SERVER_IP"
echo "  Domain    : http://$DOMAIN (after DNS propagation)"
echo ""
echo "  DB Name   : $DB_NAME"
echo "  DB User   : $DB_USER"
echo "  DB Pass   : $DB_PASSWORD"
echo ""
echo "  Logs:"
echo "    Gunicorn : journalctl -u sanjeri -f"
echo "    Nginx    : tail -f /var/log/nginx/sanjeri_error.log"
echo "    Django   : tail -f /var/log/sanjeri/error.log"
echo ""
echo "  To create admin user:"
echo "    cd $PROJECT_DIR && source venv/bin/activate"
echo "    python manage.py createsuperuser"
echo ""
echo "  To update code later:"
echo "    cd $PROJECT_DIR && git pull origin main"
echo "    source venv/bin/activate"
echo "    python manage.py migrate && python manage.py collectstatic --noinput"
echo "    systemctl restart sanjeri"
echo ""
