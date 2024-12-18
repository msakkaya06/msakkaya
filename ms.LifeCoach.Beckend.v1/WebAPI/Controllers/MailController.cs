using Business.Abstract;
using Core.Entities.Concrete;
using Core.Utilities.Results;
using Microsoft.AspNetCore.Mvc;

namespace WebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MailController : Controller
    {
        private IMailService _mailService;
        private IUserService _userService;

        public MailController(IMailService mailService, IUserService userService)
        {
            _mailService = mailService;
            _userService = userService;
        }

        [HttpGet("ResetPassword/{email}")]
        public ActionResult ResetPassword(string email)
        {
            var user = _userService.GetByMail(email);
            if (user != null)
            {
                var passwordresetlink = Url.Action("ResetPassword", "Mail", new { userId = user.Id, token = "LifeCoach" }, HttpContext.Request.Scheme);
                var result = _mailService.ResetPasswordSendMail(email, passwordresetlink);
                return Ok(result);
            }
            return NoContent();
        }
    }
}
