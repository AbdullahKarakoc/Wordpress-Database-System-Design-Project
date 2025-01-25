#!/bin/bash

# compose_1'i başlat
cd compose_1
docker-compose up -d
if [ $? -eq 0 ]; then
    echo "Compose 1 başarılı!"

    # compose_2'yi başlat
    cd ../compose_2

    # compose_2 için absolute path kullanarak çalıştır
    docker-compose -f /root/Database-Docker-Project/compose_2/docker-compose.yml up -d
    if [ $? -eq 0 ]; then
        echo "Compose 2 başarılı!"
    else
        echo "Compose 2 başarısız, kontrol ediniz."
    fi
else
    echo "Compose 1 başarısız, kontrol ediniz."
fi

