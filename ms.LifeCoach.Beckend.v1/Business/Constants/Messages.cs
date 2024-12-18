using System;
using System.Collections.Generic;
using System.Linq;
using System.Runtime.Serialization;
using System.Text;
using System.Threading.Tasks;

namespace Business.Constants
{
    public static class Messages

    {

        public static string ProductAdded = "Ürün başarıyla eklendi";
        public static string ProductDeleted = "Ürün başarıyla silindi";
        public static string ProductUpdated = "Ürün başarıyla güncellendi";
        public static string UserProfileUpdated = "Profil bilgileri başarıyla güncellendi";
        public static string UserNotFound = "Kullanıcı bulunamadı";
        public static string UserNotFoundMessage = "Mesajı alan veya gönderen kullanıcı bulunamadı";
        public static string PasswordError = "Şifre hatalı";
        public static string SuccessfulLogin = "Sisteme giriş başarılı";
        public static string UserAlreadyExists = "Bu kullanıcı zaten mevcut";
        public static string UserRegistered = "Kullanıcı başarıyla kaydedildi";
        public static string AccessTokenCreated = "Access token başarıyla oluşturuldu";
        public static string AuthorizationDenied = "Yetkiniz Yok";
        public static string ValidMessageEmail = "Geçerli bir e-posta biçimi giriniz";
        public static string ValidMessagePassword = "Şifreniz en az 6 karakterli olmalıdır";
        public static string IsAlreadyFollowed = "Kullanıcıyı zaten takip ediyorsunuz";
        public static string SuccessUserFollowed = "Takip işlemi başarılı!";
        public static string ErrorUserFollowed = "Takip işleminde hata oluştu";
        public static string SuccessUserUnfollowed = "Kullanıcıyı takibi bıraktın";
        public static string ErrorUserUnfollowed = "Takip bırakma işleminde hata oluştu";
        public static string SuccessCreatedMessage = "Mesajınız başarıyla oluşturuldu";
        public static string ErrorCreatedMessages = "Mesajınız oluşturulurken hata oluştu";
        public static string SuccessCreatedActivity = "Gönderiniz başarıyla oluşturuldu";
        public static string ErrorCreatedActivity = "Gönderiniz oluşturulurken hata oluştu";
        public static string SuccessAddedProfilePhoto = "Profil Fotoğrafı başarıyla eklendi";
        public static string ErrorAddedProfilePhoto = "Profil Fotoğrafı Eklenirken Hata oluştu";
    }
}
