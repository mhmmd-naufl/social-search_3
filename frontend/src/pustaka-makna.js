import React, { useState } from "react";
import Sidebar from "./Sidebar";
import { FiSearch } from "react-icons/fi";
import "./pustaka-makna.css";

const PustakaMakna = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [data, setData] = useState([]);
  const [filteredData, setFilteredData] = useState([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newData, setNewData] = useState({ kata: "", jenis: "kata", sentimen: "positif" });
  const [editData, setEditData] = useState(null); // State untuk data yang sedang diedit

  const handleSearch = (e) => {
    const term = e.target.value.toLowerCase();
    setSearchTerm(term);
    const filtered = data.filter((item) =>
      item.kata.toLowerCase().includes(term)
    );
    setFilteredData(filtered);
  };

  const handleUpload = (e) => {
    const file = e.target.files[0];
    if (!file.name.endsWith(".txt")) {
      alert("File harus berformat .txt");
      return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
      const text = event.target.result;

      const rows = text.split(/\r?\n/).map((row, index) => {
        const trimmedRow = row.trim();
        if (trimmedRow === "") return null;

        const parts = trimmedRow.split(",");
        if (parts.length < 3) {
          console.warn(`Baris ${index + 1} tidak valid:`, row);
          return null;
        }

        const [kata, jenis, sentimen] = parts.map((part) => part.trim());

        const validJenis = ["kata", "frasa", "emoji"];
        const validSentimen = ["positif", "negatif", "netral"];

        if (!validJenis.includes(jenis.toLowerCase())) {
          alert(`Error pada baris ${index + 1}: Jenis "${jenis}" tidak valid.`);
          return null;
        }

        if (!validSentimen.includes(sentimen.toLowerCase())) {
          alert(`Error pada baris ${index + 1}: Sentimen "${sentimen}" tidak valid.`);
          return null;
        }

        const isDuplicate = data.some((item) => item.kata.toLowerCase() === kata.toLowerCase());
        if (isDuplicate) {
          alert(`Error pada baris ${index + 1}: Data dengan "${kata}" sudah ada!`);
          return null;
        }

        return {
          id: Date.now() + Math.random(),
          kata,
          jenis,
          sentimen,
          terakhirDiperbaharui: new Date().toLocaleString(),
        };
      });

      const validRows = rows.filter((row) => row !== null);
      setData((prevData) => [...prevData, ...validRows]);
      setFilteredData((prevData) => [...prevData, ...validRows]);
    };

    reader.readAsText(file);
  };

  const handleAddData = () => {
    setEditData(null); // Reset editData untuk mode tambah
    setNewData({ kata: "", jenis: "kata", sentimen: "positif" });
    setIsModalOpen(true);
  };

  const handleEdit = (id) => {
    const dataToEdit = data.find((item) => item.id === id);
    setEditData(dataToEdit); // Set data yang akan diedit
    setNewData(dataToEdit); // Isi modal dengan data yang akan diedit
    setIsModalOpen(true);
  };

  const handleSaveData = () => {
    if (!newData.kata || !newData.jenis || !newData.sentimen) {
      alert("Semua field harus diisi!");
      return;
    }

    const isDuplicate = data.some(
      (item) =>
        item.kata.toLowerCase() === newData.kata.toLowerCase() &&
        item.id !== (editData ? editData.id : null)
    );
    if (isDuplicate) {
      alert(`Data dengan "${newData.kata}" sudah ada!`);
      return;
    }

    if (editData) {
      const updatedData = data.map((item) =>
        item.id === editData.id
          ? { ...item, ...newData, terakhirDiperbaharui: new Date().toLocaleString() }
          : item
      );
      setData(updatedData);
      setFilteredData(updatedData);
    } else {
      const newItem = {
        id: Date.now(),
        ...newData,
        terakhirDiperbaharui: new Date().toLocaleString(),
      };
      setData((prevData) => [...prevData, newItem]);
      setFilteredData((prevData) => [...prevData, newItem]);
    }

    setNewData({ kata: "", jenis: "kata", sentimen: "positif" });
    setEditData(null);
    setIsModalOpen(false);
  };

  const handleDelete = (id) => {
    const updatedData = data.filter((item) => item.id !== id);
    setData(updatedData);
    setFilteredData(updatedData);
  };

  return (
    <Sidebar>
      <div className="pustaka-makna-page container">
        <h2>Pustaka Makna</h2>
        <div className="toolbar">
          <div className="search-container">
            <input
              type="text"
              placeholder="Cari kata..."
              value={searchTerm}
              onChange={handleSearch}
            />
            <button className="search-button">
              <FiSearch />
            </button>
          </div>
          <button onClick={handleAddData}>Tambah Data</button>
          <label>
            Upload File
            <input type="file" accept=".txt" onChange={handleUpload} />
          </label>
        </div>
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
            {(searchTerm ? filteredData : data).length > 0 ? (
              (searchTerm ? filteredData : data).map((item) => (
                <tr key={item.id}>
                  <td>{item.kata}</td>
                  <td>{item.jenis}</td>
                  <td>{item.sentimen}</td>
                  <td>{item.terakhirDiperbaharui}</td>
                  <td>
                    <button
                      className="edit"
                      onClick={() => handleEdit(item.id)}
                    >
                      Edit
                    </button>
                    <button
                      className="delete"
                      onClick={() => handleDelete(item.id)}
                    >
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
        {isModalOpen && (
          <div className="modal">
            <div className="modal-content">
              <h3>{editData ? "Edit Data" : "Tambah Data Baru"}</h3>
              <input
                type="text"
                placeholder="Kata/frasa/emoji"
                value={newData.kata}
                onChange={(e) =>
                  setNewData((prev) => ({ ...prev, kata: e.target.value }))
                }
              />
              <select
                value={newData.jenis}
                onChange={(e) =>
                  setNewData((prev) => ({ ...prev, jenis: e.target.value }))
                }
              >
                <option value="kata">Kata</option>
                <option value="frasa">Frasa</option>
                <option value="emoji">Emoji</option>
              </select>
              <select
                value={newData.sentimen}
                onChange={(e) =>
                  setNewData((prev) => ({ ...prev, sentimen: e.target.value }))
                }
              >
                <option value="positif">Positif</option>
                <option value="negatif">Negatif</option>
                <option value="netral">Netral</option>
              </select>
              <button onClick={handleSaveData}>{editData ? "Simpan Perubahan" : "Simpan"}</button>
              <button onClick={() => setIsModalOpen(false)}>Batal</button>
            </div>
          </div>
        )}
      </div>
    </Sidebar>
  );
};

export default PustakaMakna;