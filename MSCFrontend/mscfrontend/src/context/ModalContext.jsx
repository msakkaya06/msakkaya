import { createContext, useContext, useState } from "react";

const ModalContext = createContext();

export const ModalProvider = ({ children }) => {
  const [content, setContent] = useState(null);

  const openModal = (node) => setContent(node);
  const closeModal = () => setContent(null);

  return (
    <ModalContext.Provider value={{ openModal, closeModal }}>
      {children}

      {content && (
        <div className="fixed inset-0 bg-black bg-opacity-40 z-50 flex items-center justify-center">
          <div className="bg-white rounded-lg p-6 w-full max-w-md shadow-xl relative">
            {content}
            <button
              onClick={closeModal}
              className="absolute top-2 right-3 text-sm text-gray-500 hover:text-black"
            >
              ✕
            </button>
          </div>
        </div>
      )}
    </ModalContext.Provider>
  );
};

export const useModal = () => {
  const ctx = useContext(ModalContext);
  if (!ctx) throw new Error("useModal() must be used inside <ModalProvider>");
  return ctx;
};
