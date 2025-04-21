import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const LogoutPage = () => {
 const businessName= localStorage.getItem("business_name");
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    const username = localStorage.getItem("username");

    // Kullanıcı bilgilerini temizle
    localStorage.removeItem("token");
    localStorage.removeItem("username");
    

    // 5 saniye sonra ana sayfaya yönlendir
    const timeout = setTimeout(() => navigate("/logout"), 5000);
    return () => clearTimeout(timeout);
  }, [navigate]);

  return (
    <div className="flex flex-col justify-center items-center h-screen bg-gray-50 text-center px-4">
      <h1 className="text-3xl font-bold text-green-700 mb-4">
      Hoşçakalın
      </h1>
      <p className="text-xl text-gray-700 mb-2">
      Bizi tercih ettiğiniz için teşekkür ederiz.
      </p>
      <p className="text-xl text-gray-600">Yine bekleriz 😊</p>
      <h3 className="text-2xl font-bold text-green-700 text-center mt-4">
      {businessName}
      <p className="text-xl text-gray-600">Yeni sipariş vermek için QR Kodu telefonunuza okutunuz.</p>

      </h3>
    </div>
  );
};

export default LogoutPage;
