EXPERIMENT="ctf-resilient-g3"
PROJECT="offtech"
ssh server.$EXPERIMENT.$PROJECT<<EOF
sudo su -
cd /etc/apache2/
touch httpd.conf
echo -e "RequestReadTimeout handshake=5 header=10 body=3\nTimeOut 5\nLimitRequestBody 1200\nLimitRequestFields 50\nLimitRequestFieldSize 4094\nLimitRequestLine 4094\n">>httpd.conf
echo -e "LoadModule cache_module modules/mod_cache.so
<IfModule mod_cache.c>
    LoadModule cache_disk_module modules/mod_cache_disk.so
    <IfModule mod_cache_disk.c>
        CacheRoot "/etc/apache2/cacheroot"
        CacheEnable disk  "/"
        CacheDirLevels 5
        CacheDirLength 3
    </IfModule>
    CacheDisable "http://security.update.server/update-list/"
</IfModule>">>httpd.conf
echo -e "<IfModule mod_cache.c>
    CacheLock on
    CacheLockPath "/tmp/mod_cache-lock"
    CacheLockMaxAge 5
</IfModule>">>httpd.conf
EOF