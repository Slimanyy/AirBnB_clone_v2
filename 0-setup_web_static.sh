#!/usr/bin/env bash
# script that sets up your web servers for the deployment of web_static

# install Nginx if not already installed
if ! command -v nginx &> /dev/null
then
    apt-get update
    apt-get install -y nginx
fi
# create the folders
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases
sudo mkdir -p /data/web_static/shared /data/web_static/releases/test /data/web_static/current
# create a fake html file
sudo echo '
<html>
  <head>
    <title>Test page</title>
  </head>
  <body>
    <p>Welcome to Nginx test page</p>
  </body>
</html>' | sudo tee /data/web_static/releases/test/index.html

# create a symbolic link
sudo ln -sf /data/web_static/current /data/web_static/releases/test/

# Give ownership of the /data/ folder to the ubuntu user
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
printf %s "server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static/ {
        alias /data/web_static/current/;
        index index.html;
    }
    
    location /redirect_me {
        return 301 https://google.com/;
    }

    error_page 404 /404.html;
    location /404 {
      root /var/www/html;
      internal;
    }
}" > /etc/nginx/sites-available/default

# restart nginx
service nginx restart
