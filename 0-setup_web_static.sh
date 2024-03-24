#!/usr/bin/env bash
# a Bash script that sets up my web servers for the deployment of web_static

#install nginx if it's not installed
if ! command -v nginx &> /dev/null; then
	sudo apt-get update
    	sudo apt-get -y install nginx
fi

# Create necessary directories if they don't exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Create a fake HTML file for testing
echo "<html>
    <head>
    </head>
    <body>hello</body>
    </html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create symbolic link /data/web_static/current
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Set ownership of /data/ directory to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content of /data/web_static/current/
sudo sed -i '/listen 80;/a \\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart

exit 0
