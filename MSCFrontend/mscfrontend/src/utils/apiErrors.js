// Hataları ve başarılı mesajları yakalayan fonksiyon
export function extractMessage(responseOrError) {
  const data = responseOrError?.response?.data || responseOrError?.data || {};

  if (typeof data === "string") return data;

  return (
    data.message ||             // ✅ Başarılı mesaj
    data.error ||               // ❌ Hata mesajı
    data.detail ||              // JWT / DRF sistem mesajı
    Object.values(data)[0] ||   // Validation error
    "Bir hata oluştu."          // Fallback
  );
}
