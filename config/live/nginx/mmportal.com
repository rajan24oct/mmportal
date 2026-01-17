server {
    server_name mindmillers.com;

    real_ip_header X-Forwarded-For;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    gzip on;
    gzip_proxied any;
    gzip_static on;
    gzip_types text/plain application/xml application/x-javascript text/javascript text/css application/x-json application/json;

    client_max_body_size 60M;
    keepalive_timeout 60;

     location /static/ {
         alias /opt/apps/mmportal/public/static/;
         expires max;
     }
     location /media/ {
         alias /opt/apps/mmportal/public/media/;
         expires max;
     }
     location /media/?(.*)$ {
         alias /opt/apps/mmportal/public/media/$host;
         expires max;
     }
    location / {
        proxy_redirect     off;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto https;

        proxy_http_version 1.1;
        proxy_set_header   Upgrade           $http_upgrade;
        proxy_set_header   Connection        "Upgrade";

    	proxy_read_timeout 500;
        proxy_connect_timeout 500;
        proxy_send_timeout 500;


        if (!-f $request_filename) {
            proxy_pass http://127.0.0.1:8000;
            break;
       }
   }
}
