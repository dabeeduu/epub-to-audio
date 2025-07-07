import React, { useState } from "react";

interface DragDropAreaProps {
  onFileSelected: (file: File) => void;
  file: File | null;
}

const DragDropArea = ({ onFileSelected, file }: DragDropAreaProps) => {
  const [dragActive, setDragActive] = useState<boolean>(false);

  const handleDrag = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();

    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onFileSelected(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onFileSelected(e.target.files[0]);
    }
  };

  return (
    <div
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
      className={`border-2 border-dashed rounded-lg p-12 text-center cursor-pointer transition-colors
        ${dragActive ? "bg-blue-50 border-blue-400" : "bg-gray-50 border-gray-300"}
      `}
    >
      <input
        type="file"
        accept=".epub"
        onChange={handleChange}
        id="fileInput"
        style={{ display: "none" }}
      />

      <label htmlFor="fileInput">
        {file
          ? `Selected :${file.name}`
          : "Drag and drop EPUB here or click to select"}
      </label>
    </div>
  );
};

export default DragDropArea;
