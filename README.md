# comentoProject
This is for how to make a chat, instagram posting web with Django, Python. Also, this project have blog function.

## Setup
To run this project, install it locally using npm:

```

npm install
npm start

```

To runserver insta
```
cd ./djangogirls
source myvenv/bin/activate
pip install -r requirements.txt
cd ../insta
python manage.py runserver 0.0.0.0:8000
```
To runserver blog
```
cd ./djangogirls
source myvenv/bin/activate
python manage.py runserver 0.0.0.0:8000
```
To chat server open

```
docker run -p 6379:6379 -d redis:5
```

## ELK
```

sudo apt-get update

sudo apt-get upgrade

sudo apt-get install default-jre

java -version

sudo apt-get install nginx

sudo systemctl start nginx

sudo systemctl status nginx

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -

echo "deb https://artifacts.elastic.co/packages/6.x/apt stable main" | sudo tee -a /etc/apt/sources.list.d/elastic-6.x.list

sudo apt-get update

sudo apt-get install elasticsearch

sudo nano /etc/elasticsearch/elasticsearch.yml

network.host: 0.0.0.0
http.cors.enabled: true
http.cors.allow-origin: "*"

sudo nano /etc/elasticsearch/jvm.options

-Xms128m
-Xmx128m

sudo systemctl start elasticsearch

sudo systemctl enable elasticsearch

sudo systemctl status elasticsearch

sudo curl -XGET http://localhost:9200

sudo apt-get install kibana

sudo systemctl start kibana

sudo systemctl enable kibana

sudo systemctl status kibana

echo "kibanaadmin:`openssl passwd -apr1`" | sudo tee -a /etc/nginx/htpasswd.users

sudo nano /etc/nginx/sites-available/<public ip>

server {
    listen 80;

    server_name <public ip>;

    auth_basic "Restricted Access";
    auth_basic_user_file /etc/nginx/htpasswd.users;

    location / {
        proxy_pass http://localhost:5601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

sudo ln -s /etc/nginx/sites-available/<public ip> /etc/nginx/sites-enabled/<public ip>

sudo nginx -t

sudo systemctl restart nginx

sudo ufw allow 'Nginx Full'

```
