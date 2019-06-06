import sys

if len(sys.argv) < 2:
    print("please specify a username")
    sys.exit(0)

user = sys.argv[1]

s = '''[{user}]
user = {user}
group = {user}
listen = /var/run/php/{user}.sock
listen.owner = www
listen.group = www
listen.mode = 0660

php_admin_value[disable_functions] = exec,passthru,shell_exec,system
php_admin_flag[allow_url_fopen] = off

pm = dynamic
pm.max_children = 5
pm.start_servers = 2
pm.min_spare_servers = 1
pm.max_spare_servers = 3
chroot = /home/{user}'''

f = open('/usr/local/php-fpm.d/' + user + '.conf', 'w+')

print(s.format(user=user))
f.write(s.format(user=user))
f.close()
