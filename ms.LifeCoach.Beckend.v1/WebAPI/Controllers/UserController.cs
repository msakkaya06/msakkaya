using Business.Abstract;
using Core.Entities.Concrete;
using DataAccess.QueryParams;
using Entities.Dtos;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;
using WebAPI.Helpers;

namespace WebAPI.Controllers
{
 
    [Route("api/[controller]")]
    [ApiController]
    public class UserController : Controller
    {
        private IUserService _userservice;

        public UserController(IUserService userService)
        {
            _userservice = userService;
          

        }
        public IActionResult Index()
        {
            return View();
        }

        [HttpGet("GetUsers")]
        public async Task<ActionResult> GetUsers([FromQuery]UserQueryParams queryParams)
        {
            
            var result = _userservice.GetAllUserById(queryParams);
            return (Ok(result));

        }
        [HttpGet("GetUser")]
        public async Task<ActionResult> GetUser(string username, int userId)
        {
            var result = _userservice.GetUser(username,userId);
            return Ok(result);

        }

        [HttpGet("GetByMail")]
        public async Task<ActionResult> GetByMail(string mail)
        {
            var result = _userservice.GetByMail(mail);
            return Ok(result);

        }
        [HttpPut("UserProfileUpdate")]
        public async Task<ActionResult> UserProfileUpdate(UserListDto user)
        {
            var result =  _userservice.UserProfileUpdate(user);
            return Ok(result);


        }
        [HttpPost("{followerUserId}/follow/{userId}")]
        public ActionResult FollowUser(int followerUserId, int userId,int accountId)
        {

            
            //if (followerUserId != accountId)
            //return Unauthorized();

            if (followerUserId == userId)
             return BadRequest("Kendini takip edemezsin");

            var IsAlreadyFollowed= _userservice.IsAlreadyFollowed(followerUserId, userId);
            if (!IsAlreadyFollowed.Success)
                return BadRequest(IsAlreadyFollowed.Message);

            var userFollowed= _userservice.UserFollow(followerUserId, userId);
            return Ok(userFollowed);

        }
        [HttpPost("{followerUserId}/unfollow/{userId}")]
        public ActionResult UnfollowUser(int followerUserId, int userId)
        {
            var userFollowed = _userservice.UserUnfollow(followerUserId, userId);
            return Ok(userFollowed);
        }
       
    }
}
