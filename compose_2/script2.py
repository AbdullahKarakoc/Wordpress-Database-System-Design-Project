import mysql.connector
from datetime import datetime
import time
import pytz

# MySQL veritabanı bağlantısı için parametreler
db_host = 'mysql_container'  
db_user = 'wp_user'  
db_password = 'wp_password'  
db_name = 'wordpress'  

time.sleep(30)

# Türkiye'nin zaman dilimini almak
tr_timezone = pytz.timezone('Europe/Istanbul')
current_time = datetime.now(tr_timezone)
formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')

# MySQL veritabanına bağlanma
conn = mysql.connector.connect(
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

# Bağlantı başarılıysa, içerik eklemeye başla
if conn.is_connected():
    print('Veritabanına bağlanıldı.')

    # Yeni paragraf içeriği
    new_paragraph = f"<p>New content added by script2.py on {formatted_time}</p>"

    # Paragraf eklemek istediğiniz post_id (ID'yi doğru almanız gerek)
    post_id = 10
    cursor = conn.cursor()

    # Eski içerik ile yeni paragrafı ekleyerek içeriği güncelleme
    cursor.execute("SELECT post_content FROM wp_posts WHERE ID = %s", (post_id,))
    result = cursor.fetchone()

    if result:
        current_content = result[0]
        updated_content = current_content + new_paragraph  # Yeni paragraf ekle

        # Veritabanındaki içeriği güncelleme
        cursor.execute("UPDATE wp_posts SET post_content = %s WHERE ID = %s", (updated_content, post_id))
        conn.commit()
        print("Blog yazısı başarıyla güncellendi.")

    cursor.close()
    conn.close()
else:
    print('Veritabanına bağlanırken hata oluştu.')

