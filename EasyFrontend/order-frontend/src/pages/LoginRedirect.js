import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import axios from "axios";

const LoginRedirect = () => {
  const [businessName, setBusinessName] = useState("");
  const [loading, setLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const token = params.get("token");
    const username = params.get("username");

    if (token && username) {
      localStorage.setItem("token", token);
      localStorage.setItem("username", username);

      const fetchBusiness = async () => {
        try {
          const res = await axios.get(
            `${process.env.REACT_APP_API_BASE_URL}/order/api/desk-info/`,
            {
              headers: {
                Authorization: `Token ${token}`,
              },
            }
          );
          localStorage.setItem("business_name", res.data.business_name);
          localStorage.setItem("desk_id",res.data.desk_id)
          setBusinessName(res.data.business_name);

          await axios.post(
            `${process.env.REACT_APP_API_BASE_URL}/order/api/create-cart/`,
            {},
            {
              headers: {
                Authorization: `Token ${token}`,
              },
            }
          );

          setLoading(false);
        } catch (err) {
          console.error("Veri alınamadı:", err);
          setHasError(true);
        }
      };

      fetchBusiness();
    } else {
      setHasError(true);
    }
  }, []);

  if (loading) {
    return <div className="text-center mt-20 text-xl">Giriş yapılıyor...</div>;
  }

  if (hasError) {
    return (
      <div className="text-center mt-20 text-red-500 font-bold text-xl">
        Giriş başarısız. Lütfen QR kodu tekrar okutun.
      </div>
    );
  }

  return (
    <div className="text-center mt-20">
      <h1 className="text-2xl font-bold mb-4">
        {businessName} Hoşgeldiniz!
      </h1>
      <p className="mb-4 text-lg">Menümüze ulaşmak için aşağıya tıklayabilirsiniz.</p>
      <Link
        to="/"
        className="bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded inline-block"
      >
        Menüyü Aç
      </Link>
    </div>
  );
};

export default LoginRedirect;
