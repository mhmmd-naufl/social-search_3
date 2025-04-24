import React, { useState } from "react";
import Sidebar from "./Sidebar";
import "./pustaka-makna.css";

const PustakaMakna = () => {
  const [searchTerm, setSearchTerm] = useState(""); // State untuk pencarian
  const [data, setData] = useState([]); // State untuk data tabel

  // Fungsi untuk menangani pencarian
  const handleSearch = (e) => {
    setSearchTerm(e.target.value);
  };

  // Fungsi untuk menangani upload file
  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file.name.endsWith(".txt")) {
        alert("File harus berformat .txt");
        return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
        console.log("File berhasil dibaca"); // Debug: Periksa apakah file berhasil dibaca
      const text = event.target.result;

      console.log("Isi file:", JSON.stringify(text)); // Debug: Periksa isi file

      const rows = text.split(/\r?\n/).map((row, index) => {
        const trimmedRow = row.trim();
        if (trimmedRow === "") return null; // Lewati baris kosong
      
        const parts = trimmedRow.split(",");
        if (parts.length < 3) {
          console.warn(`Baris ${index + 1} tidak valid:`, row);
          return null;
        }
      
        const [kata, jenis, sentimen] = parts;
      
        return {
          id: Date.now() + Math.random(),
          kata: kata.trim(),
          jenis: jenis.trim(),
          sentimen: sentimen.trim(),
          terakhirDiperbaharui: new Date().toLocaleString(),
        };
      });

      const validRows = rows.filter((row) => row !== null); // Hanya ambil baris yang valid
      console.log("Data yang diformat:", validRows); // Debug: Periksa data yang diformat

      setData((prevData) => [...prevData, ...validRows]); // Tambahkan data ke state
    };

    reader.readAsText(file); // Baca file sebagai teks
  };

  // Fungsi untuk menambah data baru (placeholder)
  const handleAddData = () => {
    console.log("Tambah data baru");
  };

  // Fungsi untuk mengedit data (placeholder)
  const handleEdit = (id) => {
    console.log("Edit data dengan ID:", id);
  };

  // Fungsi untuk menghapus data
  const handleDelete = (id) => {
    const updatedData = data.filter((item) => item.id !== id);
    setData(updatedData);
  };

  console.log("Data di tabel:", data); // Debug: Periksa isi state data

  return (
    <Sidebar>
      <div className="pustaka-makna-page container">
        <h2>Pustaka Makna</h2>

        {/* Tombol dan Search Bar */}
        <div className="toolbar">
          <input
            type="text"
            placeholder="Cari kata..."
            value={searchTerm}
            onChange={handleSearch}
          />
          <button onClick={handleAddData}>Tambah Data</button>
          <label>
            Upload File
            <input type="file" accept=".txt" onChange={handleUpload} />
          </label>
        </div>

        {/* Tabel */}
        <table>
          <thead>
            <tr>
              <th>Kata/frasa/emoji</th>
              <th>Jenis</th>
              <th>Sentimen</th>
              <th>Terakhir Diperbarui</th>
              <th>Aksi</th>
            </tr>
            </thead>
  <tbody>
    {data.length > 0 ? (
      data.map((item) => (
        <tr key={item.id}>
          <td>{item.kata}</td>
          <td>{item.jenis}</td>
          <td>{item.sentimen}</td>
          <td>{item.terakhirDiperbaharui}</td>
          <td>
            <button className="edit" onClick={() => handleEdit(item.id)}>
              Edit
            </button>
            <button className="delete" onClick={() => handleDelete(item.id)}>
              Hapus
            </button>
          </td>
        </tr>
      ))
    ) : (
      <tr>
        <td colSpan="5">Tidak ada data</td>
      </tr>
    )}
  </tbody>
        </table>
      </div>
    </Sidebar>
  );
};

export default PustakaMakna