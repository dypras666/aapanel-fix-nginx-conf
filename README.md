# aaPanel Nginx Configuration Fixer

🇮🇩 [Bahasa Indonesia](#panduan-bahasa-indonesia) | 🇺🇸 [English](#english-guide)

## Panduan Bahasa Indonesia

Script Python untuk memperbaiki konfigurasi Nginx di aaPanel yang rusak atau tidak terstruktur. Script ini dirancang khusus untuk menangani masalah umum pada konfigurasi Nginx di aaPanel seperti location blocks yang terduplikasi atau salah posisi.

### ✨ Fitur Utama
- Memperbaiki semua file konfigurasi Nginx sekaligus
- Menangani file 0.default.conf secara khusus
- Membuat backup otomatis sebelum melakukan perubahan
- Memeriksa keberadaan file rewrite
- Mempertahankan versi PHP dan root path yang sudah ada
- Merapikan struktur dan indentasi konfigurasi

### 🚀 Cara Penggunaan

1. Download script:
```bash
wget https://raw.githubusercontent.com/dypras666/aapanel-fix-nginx-conf/main/fix_nginx_all.py
```

2. Berikan izin eksekusi:
```bash
chmod +x fix_nginx_all.py
```

3. Jalankan script:
```bash
python3 fix_nginx_all.py
```

4. Verifikasi konfigurasi:
```bash
nginx -t
```

5. Jika tidak ada error, restart Nginx:
```bash
/etc/init.d/nginx restart
```

### ⚙️ Apa yang Diperbaiki?
- Struktur server block yang benar
- Penempatan location blocks yang tepat
- Penanganan file rewrite yang benar
- Format dan indentasi yang konsisten
- Konfigurasi khusus untuk 0.default.conf

### 🔄 Cara Mengembalikan Perubahan
Script membuat backup otomatis dengan format: `.backup_[timestamp]`
```bash
# Contoh mengembalikan konfigurasi
cp domain.com.conf.backup_20241230_123456 domain.com.conf
```

### ⚠️ Peringatan
- Selalu backup data penting sebelum menggunakan script
- Pastikan memeriksa hasil konfigurasi dengan `nginx -t`
- Jika terjadi masalah, gunakan file backup untuk mengembalikan konfigurasi

---

## English Guide

Python script to fix broken or unstructured Nginx configurations in aaPanel. This script is specifically designed to handle common Nginx configuration issues in aaPanel such as duplicated or misplaced location blocks.

### ✨ Key Features
- Fixes all Nginx configuration files at once
- Special handling for 0.default.conf
- Creates automatic backups before making changes
- Checks for rewrite file existence
- Maintains existing PHP versions and root paths
- Cleans up structure and indentation

### 🚀 How to Use

1. Download the script:
```bash
wget https://raw.githubusercontent.com/dypras666/aapanel-fix-nginx-conf/main/fix_nginx_all.py
```

2. Make it executable:
```bash
chmod +x fix_nginx_all.py
```

3. Run the script:
```bash
python3 fix_nginx_all.py
```

4. Verify configuration:
```bash
nginx -t
```

5. If no errors, restart Nginx:
```bash
/etc/init.d/nginx restart
```

### ⚙️ What Gets Fixed?
- Proper server block structure
- Correct location blocks placement
- Proper rewrite file handling
- Consistent formatting and indentation
- Special configuration for 0.default.conf

### 🔄 How to Rollback Changes
Script creates automatic backups with format: `.backup_[timestamp]`
```bash
# Example of reverting configuration
cp domain.com.conf.backup_20241230_123456 domain.com.conf
```

### ⚠️ Warning
- Always backup important data before using the script
- Make sure to check configuration with `nginx -t`
- If issues occur, use backup files to restore configuration

## 🔧 Technical Details

### Default Configuration (0.default.conf)
```nginx
server {
    listen 80;
    server_name _;
    index index.html;
    root /www/server/nginx/html;
}
```

### Domain Configuration Template
```nginx
server {
    listen 80;
    server_name example.com;
    root /www/wwwroot/example.com;
    # ... other configurations
}
```

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check [issues page](https://github.com/dypras666/aapanel-fix-nginx-conf/issues).

## 📝 License
This project is [MIT](https://opensource.org/licenses/MIT) licensed.

## 🏷️ Tags
`aapanel` `nginx` `configuration` `optimization` `server` `web-server` `fix` `automation` `python` `script` `devops` `sysadmin` `hosting` `server-management` `linux`