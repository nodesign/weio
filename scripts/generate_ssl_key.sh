#openssl genrsa -out weioSSL.key 2048
#openssl req -new -key weioSSL.key -out weioSSL.csr

if [ ! -e weioSSL.csr ]; then
    openssl req -nodes -newkey rsa:2048 -keyout weioSSL.key -out weioSSL.csr -subj "/C=FR/ST=Paris/L=Paris/O=WeIO/OU=IoT/CN=we-io.net"
fi


if [ ! -e weioSSL.crt ]; then
    openssl x509 -req -days 365 -in weioSSL.csr -signkey weioSSL.key -out weioSSL.crt
fi
