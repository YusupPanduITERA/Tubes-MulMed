# TUGAS BESAR MULTIMEDIA IF4021
*Reaction Time* 

## Anggota Kelompok 
|         Nama Anggota      |    Nim    |         ID Github       |
|---------------------------|-----------|------------------------ |
| Yusup Pandu Putra Wibowo  | 121140124 |     YusupPanduITERA     |


## Deskripsi
"Reaction Time"
Aplikasi ini menguji reaksi pengguna terhadap instruksi dengan memanfaatkan pengenalan wajah secara real-time, menampilkan gambar tersegmentasi, dan menghitung kesamaan antara gambar untuk memberikan nilai akurasi.
- OpenCV: Untuk manipulasi video dan rendering efek visual.
- MediaPipe: Untuk deteksi wajah secara real-time dan pengolahan landmark wajah.
- NumPy: Untuk perhitungan matematis.

## Fitur Utama 
1. Pengujian Reaksi Wajah 
- Menginstruksikan pengguna untuk mengangguk sebagai respons terhadap instruksi yang diberikan.
- Melacak pergerakan wajah dan mendeteksi gerakan mengangguk menggunakan landmark wajah.

 2. Segmentasi Gambar
- Memuat gambar referensi, membagi menjadi dua bagian (kiri dan kanan), dan memadukan bagian tersebut dengan posisi wajah pengguna pada video secara dinamis.

 3. Perhitungan Akurasi
- Menghitung tingkat kesamaan antara bagian kiri dan kanan gambar dengan menggunakan teknik perbedaan piksel untuk menentukan nilai akurasi pengguna.

 4. Tampilan Dinamis
- Menampilkan instruksi pada layar dengan efek overlay.
- Memutar gambar kanan dengan animasi rotasi.

## Hasil Akhir
Filter video secara realtime dengan menguji keakurasian pengguna dalam akurasi ketepatan gambar. 

## Logbook Mingguan
|No | Minggu  |              Progress           |
|---|---------|---------------------------------|
| 1 | Pertama | Belum Ada Progress              |
| 2 | Kedua   | Dalam Pengerjaan Untuk Kodenya  |
| 3 | Ketiga  | Penyempurnaan Kode              |

## Instruksi Instalasi dan Penggunaan  

## 1. Requirements
Persyaratan Sistem:
Webcam untuk pengambilan video real-time.
Python 3.7.xx - 3.10.xx .
Sebuah image file. 

## 2. Instalasi  
1. Clone repositori ini ke komputer Anda:  
   ```bash  
   git clone https://github.com/YusupPanduITERA/Tubes-MulMed 
   cd Tubes-MulMed
    ```
2. Instal dependensi menggunakan requirements.txt:  
   ```bash  
   pip install -r requirements.txt  
    ```
### 3. Menjalankan Program
1. Jalankan file utama menggunakan Python:  
   ```bash  
    python main.py 
    ```
2. Arahkan wajah anda kekamera dan ikuti instruksi di filter.
