using Business.Abstract;

using Core.Utilities.RealTimeChat.SignalR;
using Core.Entities.Concrete.Dto;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.SignalR;
using System.Security.Claims;
using Core.Entities.Concrete;
using Business.DependencyResolvers.SignalR.HubConfig;

namespace WebAPI.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class MessageController : Controller
    {
        private IMessageService _messageService;
        private readonly IHubContext<ChatHub> _hub;
        private readonly TimerManager _timer;

        public MessageController(IMessageService messageService, IHubContext<ChatHub> hub, TimerManager timer)
        {
            _messageService = messageService;
            _hub = hub;
            _timer = timer;

        }

        [HttpPost("CreateMessage/{userId}")]
        public ActionResult CreateMessage(int userId, MessageForCreateDto messageForCreateDto)
        {
            messageForCreateDto.SenderId = userId;
            var recipient = _messageService.UserExist(messageForCreateDto.RecipientId);
            var sender = _messageService.UserExist(messageForCreateDto.SenderId);
            if (sender.Success && recipient.Success)
            {
                var message = _messageService.CreateMessage(messageForCreateDto);

                if (message.Success)
                {
                    return Ok(message.Message);
                }
                else
                {
                    return BadRequest(message);
                }
            }
            if (!sender.Success) return BadRequest(sender.Message);

            return BadRequest(recipient.Message);

        }

        [HttpGet("GetMessage/{userId}")]
        public ActionResult GetMessageList(int userId)
        {
            var result = _messageService.GetMessageList(userId);
            if (result.Success)
            {
                return Ok(result);
            }
            return NoContent();
        }



        [HttpGet("GetMessageUserList/{userId}")]
        public ActionResult GetMessageUserList(int userId)
        {
            var result = _messageService.GetMessageUserList(userId);
            if (result != null)
            {
                return Ok(result);
            }
            return NoContent();
        }

        [HttpGet("GetUsersChat/{userId}/{friendUserId}")]
        public ActionResult GetMessageUserList(int userId, int friendUserId)
        {

            var result = _messageService.GetUsersChat(userId, friendUserId, false);
            if (result != null)
            {
                return Ok(result);
            }
            return NoContent();
        }
        //SignalR kullanılarak gerçekleştirilen metot
        [HttpGet("GetUsersChatRT/{userId}/{friendUserId}")]
        public ActionResult GetUsersChatRT(int userId, int friendUserId)
        {
            if (!_timer.IsTimerStarted)
                _timer.PrepareTimer(() => _hub.Clients.All.SendAsync("TransferChatData", _messageService.GetUsersChat(userId, friendUserId, true)));
            return Ok(new { Message = "Request Completed" });

        }
        [HttpPost("SetUsersConnectionIds")]
        public ActionResult SetUsersConnectionIds(UsersConnectionIds usersConnectionIds)
        {
            usersConnectionIds.ConnectedDate = DateTime.Now;
            var result = _messageService.SetUsersConnectionIds(usersConnectionIds);
            if (result != null) { return Ok(result); }
            return NoContent();
        }
    }
}
