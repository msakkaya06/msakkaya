using Azure.Core.Serialization;
using Business.Abstract;
using Entities.Dtos;
using Microsoft.AspNetCore.DataProtection.XmlEncryption;
using Microsoft.AspNetCore.Http.HttpResults;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;
using Swashbuckle.AspNetCore.SwaggerGen;
using System;
using System.Runtime.InteropServices.JavaScript;
using System.Text.Json.Serialization;

namespace WebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ActivityController : Controller
    {
        private IActivityService _activityService;
        public ActivityController(IActivityService activityService)
        {
            _activityService = activityService;
        }
        public IActionResult Index()
        {
            return View();
        }

        [HttpGet("GetFollowingUsersActivity/{userId}")]
        public ActionResult GetFollowingUsersActivity(int userId)
        {
            var result = _activityService.GetFollowingUsersActivity(userId);
            if (result != null) return Ok(result);
            return NoContent();

        }


        [HttpPost("AddActivity/{userId}")]
        public ActionResult AddActivity(int userId, Object data)
        {
            JObject dataParse = JObject.Parse(data.ToString());
            JArray dataArray = (JArray)dataParse["photoForCreationDto"];
            List<PhotoForActivity> photoList = dataArray.ToObject<List<PhotoForActivity>>();
            var res = _activityService.AddActivity(userId, photoList);
            if (res.Success) return Ok(res);
            return Ok();
        }


        [HttpGet("GetUserActivity/{userId}")]
        public ActionResult GetUserActivity(int userId)
        {
            var result = _activityService.GetUserActivity(userId);
            if (result != null) return Ok(result);
            return NoContent();

        }
        [HttpPost("AddComment/{activityId}/{userId}")]
        public ActionResult AddComment(int userId, int activityId, CreateCommentDto createCommentDto)
        {
            createCommentDto.UserId = userId;
            createCommentDto.ActivityId = activityId;
            var result = _activityService.AddComment(createCommentDto);
            if (result.Success) return Ok(result);
            return NoContent();

        }

        [HttpGet("GetComments/{activityId}")]
        public ActionResult GetComments(int activityId)
        {
            var result = _activityService.GetCommentsActivity(activityId);
            if (result != null) return Ok(result);
            return NoContent();
        }
    }
}
