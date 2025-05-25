### ERD
![Screen Shot 2025-05-25 at 11 48 45](https://github.com/user-attachments/assets/738faf0b-3928-46bc-8bbe-096d332a555f)

### Fitur
- CRUD data material (`test.material`)
- Endpoint API untuk Create, Read, Update, dan Delete
- Format response konsisten dalam JSON
- Unit test untuk semua endpoint

### Instalasi
1. Clone repositori berikut
   ```bash
   git clone https://github.com/rizalbachtiar/odoo_dev_test.git
2. Jalankan Odoo dan install modul
   ```bash
   ./odoo-bin -c nama_config.conf -d nama_database -u test_material

### Unit Test
Unit test berada di folder tests/. Untuk menjalankan
```bash
   ./odoo-bin -c nama_config.conf -d nama_database --test-tags test_material

