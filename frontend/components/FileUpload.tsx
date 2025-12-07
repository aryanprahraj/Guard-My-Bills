import React, { useRef } from 'react';

interface FileUploadProps {
  onUpload: (file: File) => void;
  loading?: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ onUpload, loading }) => {
  const inputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      onUpload(e.target.files[0]);
    }
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      onUpload(e.dataTransfer.files[0]);
    }
  };

  return (
    <div
      className={`border-2 border-dashed rounded p-6 text-center cursor-pointer bg-white ${loading ? 'opacity-50' : ''}`}
      onClick={() => inputRef.current?.click()}
      onDrop={handleDrop}
      onDragOver={e => e.preventDefault()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".csv"
        className="hidden"
        onChange={handleFileChange}
        disabled={loading}
      />
      <div className="text-gray-700">
        {loading ? 'Uploading...' : 'Drag & drop or click to select a CSV file'}
      </div>
    </div>
  );
};

export default FileUpload;
