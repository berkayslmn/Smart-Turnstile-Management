# Smart Turnstile Management System

## Proje Hakkında ve Amacı
Bu proje, stadyumlar, konser alanları, festivaller ve büyük ölçekli organizasyonlar gibi yoğun insan hareketliliğinin olduğu alanlarda turnike ve geçiş kontrol süreçlerini modernize etmek amacıyla geliştirilmiş uçtan uca bir akıllı yönetim sistemidir. Geleneksel geçiş sistemlerinin aksine, binlerce katılımcının aynı anda giriş yapmaya çalıştığı senaryolarda kilitlenmeleri önlemek, geçiş doğrulamalarını milisaniyeler içinde gerçekleştirmek ve tüm operasyonel hareketliliği güvenli bir veri altyapısında loglamak üzere tasarlanmıştır.

Kullanılan Teknolojiler (Tech Stack)
* **Backend:** Python (Flask)
* **Database:** Firebase, Supabase
* **Frontend:** HTML/CSS, Jinja2 (Templates)
* **Core:** Algoritmik doğrulama ve QR Code işleme

Sistem, bilet veya yetki belgesi niteliğindeki QR kodların taranması, bu kodların anlık olarak doğrulanması ve fiziksel turnike tetikleme mekanizmalarına veri sağlanması temel prensibiyle çalışır.

## Veritabanı Mimarisi ve Kullanılan Eklentiler (Database & Extensions)
Proje, yüksek erişilebilirlik, hız ve veri bütünlüğü sağlamak amacıyla hibrit bir veritabanı ve eklenti mimarisi üzerine kurulmuştur:

* **Supabase (PostgreSQL Tabanlı İlişkisel Veritabanı):** Kullanıcı rolleri, yetkilendirme matrisleri ve detaylı geçiş loglarının kalıcı olarak saklanması amacıyla ilişkisel (relational) bir yapı sunar. Güçlü SQL sorgulama yetenekleri sayesinde geçmişe dönük raporlama ve analiz süreçlerini destekler.
* **Firebase (Bulut Veritabanı ve Senkronizasyon):** Anlık veri akışının kritik olduğu durumlarda hızlı okuma/yazma operasyonları ve anlık istemci senkronizasyonu için entegre edilmiştir. Turnike noktalarından gelen anlık sinyallerin merkeze gecikmesiz iletilmesini sağlar.
* **Yerel Doğrulama ve Loglama Eklentileri (`valid_qrs`, `gecis_log`):** Bulut bağlantısında olası kesintiler durumunda sistemin kesintisiz çalışabilmesi (offline-first yaklaşımı) ve yerel testlerin hızlıca koşturulabilmesi için JSON tabanlı doğrulama listeleri ve metin tabanlı loglama modülleri barındırır.
* **QR Kod İşleme Motoru (`qr_creator.py`):** Python tabanlı kütüphaneler aracılığıyla her katılımcı için benzersiz, şifrelenmiş ve kopyalanamaz QR kod matrisleri üretir.

## Modül Yapısı ve Dosya Açıklamaları
* `app.py`: Flask tabanlı web sunucusu olup, arayüz isteklerini, yönlendirmeleri ve API uç noktalarını (endpoints) yönetir.
* `turnike.py`: Geçiş kontrol algoritmasının çalıştığı, gelen QR kodun veritabanındaki geçerlilik kurallarına göre sorgulandığı ve turnike tetikleme kararının verildiği çekirdek mantık (core logic) modülüdür.
* `qr_creator.py`: Yetkili girişler için benzersiz QR kod matrislerinin üretilmesini ve biçimlendirilmesini sağlar.
* `gecis_log`: Sistem üzerinden gerçekleşen başarılı veya başarısız tüm geçiş denemelerinin zaman damgasıyla birlikte kaydedildiği log dosyasıdır.

## Güvenlik ve Kapsam Notu (Security & Scope Note)
* **Güvenlik (Security):** Güvenlik politikaları gereği, hassas API anahtarları, proje kimlik bilgileri ve gizli bağlantı parametreleri içeren veritabanı yapılandırma dosyaları (`firebase_config`, `supabase_config.py`) ile saha operasyonlarına ait gerçek kişisel ve doğrulama verilerini barındıran (`valid_qrs`) dosyaları bu açık depoya (public repository) dahil edilmemiştir.
* **Kapsam (Scope):** Deponun tamamen arka plan (backend) mimarisine, veritabanı yönetimine, hibrit entegrasyonlara ve geçiş algoritması mantığına odaklanması amacıyla arayüz bileşenleri (`static/`, `templates/`) kapsam dışında bırakılmıştır.

## Kurulum ve Çalıştırma Adımları
1. Projeyi yerel bilgisayarınıza klonlayın:
   ```bash
   git clone [https://github.com/berkayslmn/Smart-Turnstile-Management.git](https://github.com/berkayslmn/Smart-Turnstile-Management.git)


