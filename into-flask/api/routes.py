from sqlalchemy.orm import joinedload # Mengimpor `joinedload` untuk eager loading
from flask import request, jsonify # Mengimpor objek `request` untuk menangkap data dari request, dan`jsonify` untuk mengembalikan data JSON
from app import app, db # Mengimpor objek `app` dan `db` dari modul `app`
from models import Fakultas, Prodi, Mahasiswa # Mengimpor model Fakultas, Prodi, dan Mahasiswa





@app.route('/api/fakultas', methods=['GET']) # Endpoint untuk mendapatkan semua data Fakultas
def get_fakultas():
    fakultas = Fakultas.query.all() # Query untuk mendapatkan semua data Fakultas dari database
    output = []
    for fac in fakultas: # Iterasi setiap Fakultas
        prodi_list = [{'id': prodi.id, 'nama': prodi.nama} for prodi in fac.prodis]# Mendapatkan daftar Prodi terkait
    output.append({
        'id': fac.id,
        'nama': fac.nama,
        'prodi': prodi_list # Tambahkan data Prodi ke dalam fakultas 
    })
    return jsonify(output) # Mengembalikan data Fakultas dalam format JSON

@app.route('/api/fakultas', methods=['POST']) # Endpoint untuk menambahkan Fakultas baru
def add_fakultas():
        data = request.get_json() # Mendapatkan data JSON dari body request
        if 'nama' not in data: # Validasi jika data tidak memiliki key `nama`
            return jsonify({'message': 'Nama fakultas diperlukan'}), 400 # Mengembalikan error jika validasi gagal
        fakultas = Fakultas(nama=data['nama']) # Membuat objek Fakultas baru
        db.session.add(fakultas) # Menambahkan data Fakultas ke session database
        db.session.commit() # Menyimpan perubahan ke database
        return jsonify({'message': 'Fakultas berhasil ditambahkan'}), 201 # Mengembalikan pesan berhasil

@app.route('/api/fakultas/<int:id>', methods=['PUT']) # Endpoint untuk memperbarui data Fakultas
def update_fakultas(id):
        fakultas = Fakultas.query.get(id) # Mencari Fakultas berdasarkan id
        if not fakultas: # Jika Fakultas tidak ditemukan
             return jsonify({'message': 'Fakultas tidak ditemukan'}), 404 # Mengembalikan error jika Fakultas tidak
        ditemukan
        data = request.get_json() # Mendapatkan data JSON dari body request
        if 'nama' in data: # Jika ada field 'nama' dalam data yang diterima
            fakultas.nama = data['nama'] # Update nama Fakultas dengan nilai yang diterima
        db.session.commit() # Menyimpan perubahan ke database
        return jsonify({'message': 'Fakultas berhasil diperbarui'}), 200 # Mengembalikan pesan berhasil

@app.route('/api/fakultas/<int:id>', methods=['DELETE']) # Endpoint untuk menghapus Fakultas
def delete_fakultas(id):
        fakultas = Fakultas.query.get(id) # Mencari Fakultas berdasarkan id
        if not fakultas: # Jika Fakultas tidak ditemukan
             return jsonify({'message': 'Fakultas tidak ditemukan'}), 404 # Mengembalikan error jika Fakultas tidak
        ditemukan
        # Opsional: Cek apakah masih ada Prodi yang terkait dengan Fakultas ini
        if fakultas.prodis:
              return jsonify({'message': 'Fakultas tidak bisa dihapus karena masih memiliki Prodi terkait'}), 400
        db.session.delete(fakultas) # Menghapus Fakultas dari database
        db.session.commit() # Menyimpan perubahan ke database
        return jsonify({'message': 'Fakultas berhasil dihapus'}), 200 # Mengembalikan pesan berhasil

@app.route('/api/prodi', methods=['GET']) # Endpoint untuk mendapatkan semua data Prodi
def get_prodi():
        prodis = Prodi.query.options(joinedload(Prodi.fakultas)).all()
        # Query semua data Prodi dengan eager loading untuk data Fakultas terkait
        output = []
        for prodi in prodis: # Iterasi setiap Prodi
            output.append({
        'id': prodi.id,
        'nama': prodi.nama,
        'fakultas_id': prodi.fakultas_id,
        'fakultas_nama': prodi.fakultas.nama # Menambahkan nama Fakultas terkait
        })
        return jsonify(output) # Mengembalikan data Prodi dalam format JSON

@app.route('/api/prodi', methods=['POST']) # Endpoint untuk menambahkan Prodi baru
def add_prodi():
        data = request.get_json() # Mendapatkan data JSON dari body request
        if 'nama' not in data or 'fakultas_id' not in data: # Validasi jika data tidak memiliki key `nama` atau`fakultas_id`
         return jsonify({'message': 'Nama prodi dan fakultas_id diperlukan'}), 400 # Mengembalikan error jikavalidasi gagal
        fakultas = Fakultas.query.get(data['fakultas_id']) # Validasi jika Fakultas terkait ada
        if not fakultas:
            return jsonify({'message': 'Fakultas tidak ditemukan'}), 404 # Mengembalikan error jika Fakultas tidak
        ditemukan
        prodi = Prodi(nama=data['nama'], fakultas_id=data['fakultas_id']) # Membuat objek Prodi baru
        db.session.add(prodi) # Menambahkan data Prodi ke session database
        db.session.commit() # Menyimpan perubahan ke database
        return jsonify({'message': 'Prodi berhasil ditambahkan'}), 201 # Mengembalikan pesan berhasil