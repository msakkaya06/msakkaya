using Business.Abstract;
using Business.DependencyResolvers.RabbitMQ;
using Core.Utilities.Results;
using DataAccess.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.Concrete
{
    public class MailManager : IMailService
    {
        IUserService _userService;
       RabbitMQHelper _rabbitMQHelper;
       PasswordResetRequestHandler _passwordResetRequestHandler;
        public MailManager(IUserService userService, RabbitMQHelper rabbitMQHelper, PasswordResetRequestHandler passwordResetRequestHandler)
        {
           
            _userService = userService;
            _rabbitMQHelper = rabbitMQHelper;
            _passwordResetRequestHandler = passwordResetRequestHandler;
        }
        public IResult ResetPasswordSendMail(string email, string resetPasswordLink)
        {
            _rabbitMQHelper.SendPasswordResetRequest(email, resetPasswordLink);
            _passwordResetRequestHandler.StartHandling();
            return new SuccessResult("Şifre Sıfırlama E-Posta Gönderildi");
        }

    }
}
