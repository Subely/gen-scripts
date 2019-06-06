import sys

if len(sys.argv) < 3:
    print("please specify a username and url")
    sys.exit(0)

user = sys.argv[1]
url = sys.argv[2]

s = '''server {{
listen 80;
root /home/{user}/public_html;

    server_name {url};

	index index.html index.php;

	location / {{
        try_files $uri $uri/ /index.php?$query_string;
    }}

	location ~ \.php$ {{
		try_files $uri =404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
		fastcgi_pass unix:/var/run/php/{user}.sock;
        fastcgi_index index.php;
        fastcgi_param SCRIPT_FILENAME $document_root/$fastcgi_script_name;
        include fastcgi_params;
    }}

}}'''

f = open('/usr/local/nginx/users/' + user + '_' + url +'.conf', 'w+')

print(s.format(user=user))
f.write(s.format(user=user))
f.close()
