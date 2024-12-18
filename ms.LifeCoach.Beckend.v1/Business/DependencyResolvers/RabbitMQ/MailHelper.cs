using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Mail;
using System.Text;
using System.Threading.Tasks;

namespace Business.DependencyResolvers.RabbitMQ
{
    public class MailHelper
    {
        public static void PasswordSendMail(string link,string mailAdress)
        {
            MailMessage mail = new MailMessage();

            SmtpClient smtp = new SmtpClient();

            mail.From = new MailAddress("lc.msakkaya@gmail.com");

            mail.To.Add(mailAdress);

            mail.Subject = "Şifre güncelleme talebi";

            mail.Body = "<h2>Şifrenizi yenilemek için linke tıklayınız </h2> <hr>";
            mail.Body += $"<a href='{link}'> Şifre yenileme bağlantısı";

            mail.IsBodyHtml = true;
            smtp.Host = "smtp.gmail.com";
            smtp.Port = 587;
            smtp.EnableSsl = true;
            smtp.Credentials = new System.Net.NetworkCredential("lc.msakkaya@gmail.com", "yuxmuvvdqnwvqoos");
            smtp.Send(mail);

        }
    }
}
