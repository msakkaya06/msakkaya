using Business.Abstract;
using Core.Aspects.Autofac.Exception;
using Core.CrossCuttingConcerns.Logging.Log4Net.Loggers;
using DataAccess.QueryParams;
using Entities.Dtos;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Identity.Client.Platforms.Features.DesktopOs.Kerberos;
using System.Drawing;
using System.Net.Sockets;

namespace WebAPI.Controllers
{
    [Route("api/photos/")]
    [ApiController]
    [Produces("application/json")]
    public class PhotoController : Controller
    {

       public IPhotoService _photoService;
        private readonly IWebHostEnvironment _environment;
        public PhotoController(IPhotoService photoService, IWebHostEnvironment environment)
        {
            _photoService = photoService;
            _environment = environment; 

            
        }
        public IActionResult Index()
        {
            return View();
        }

        [HttpPost("{userId}")]
        public ActionResult AddProfilePhoto(int userId,[FromForm] PhotoForCreationDto photoForCreationDto)
        {
            var res = _photoService.AddProfilePhoto(userId, photoForCreationDto);
            if (res!=null) return Ok(res);
            return BadRequest(res);
        }

        [HttpPost("AddPost/{userId}")]
        public ActionResult AddPost(int userId, [FromForm] PhotoForCreationDto photoForCreationDto)
        {
            var res = _photoService.AddPost(userId, photoForCreationDto);
            if (res != null) return Ok(res);
            return BadRequest(res);
        }


        [HttpPost("AddImage/{userId}")]
        public ActionResult AddImage(int userId, [FromForm] PhotoForCreationDto photoForCreationDto)
        {
            var res = _photoService.AddImage(userId, photoForCreationDto);
            if (res != null) return Ok(res);
            return BadRequest(res);
        }

        [HttpPost("Add")]
        public async Task<IActionResult> SaveTicket(Ticket ticket, [FromForm] Image  File)
        {
            return Ok(ticket);
        }
        }
}