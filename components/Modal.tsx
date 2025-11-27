import React, { ReactNode } from 'react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  children: ReactNode;
  title?: string;
}

const Modal: React.FC<ModalProps> = ({ isOpen, onClose, children, title }) => {
  if (!isOpen) return null;
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40">
      <div className="bg-white rounded-2xl shadow-xl max-w-lg w-full p-6 relative animate-fadeIn">
        <button
          className="absolute top-4 right-4 text-gray-400 hover:text-gray-700 text-2xl"
          onClick={onClose}
          aria-label="Close"
        >
          &times;
        </button>
        {title && <div className="text-xl font-semibold mb-4 text-center">{title}</div>}
        {children}
      </div>
    </div>
  );
};

export default Modal;
