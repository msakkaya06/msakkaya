using AutoMapper;
using Business.Abstract;
using Business.Constants;
using Core.Entities.Concrete;
using Core.Entities.Concrete.Dto;
using Core.Utilities.Results;
using DataAccess.Abstract;
using DataAccess.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Security.Cryptography.X509Certificates;
using System.Text;
using System.Threading.Tasks;

namespace Business.Concrete
{
    public class MessageManager : IMessageService
    {
        IUserService _userService;
        IMapper _mapper;
        IMessageDal _messageDal;
        public MessageManager(IUserService userService, IMapper mapper, IMessageDal messageDal)
        {

            _userService = userService;
            _mapper = mapper;
            _messageDal = messageDal;

        }

        public IDataResult<MessageForCreateDto> CreateMessage(MessageForCreateDto messageForCreateDto)
        {

            var message = _mapper.Map<Message>(messageForCreateDto);
            var result = _messageDal.CreateMessage(message);
            if (result)
            {
                var messageDto = _mapper.Map<MessageForCreateDto>(message);
                return new SuccessDataResult<MessageForCreateDto>(messageDto, Messages.SuccessCreatedMessage);

            }
            return new ErrorDataResult<MessageForCreateDto>(messageForCreateDto, Messages.ErrorCreatedMessages);

        }

        public IDataResult<List<MessageListDto>> GetMessageList(int CurrentUserId)
        {
            var result = new List<MessageListDto>();
            var resultUser = new MessageListDto();
            var sendedMessageList = _messageDal.GetSendedMessageList(CurrentUserId);
            var receivedMessagelist = _messageDal.GetReceivedMessageList(CurrentUserId);
            if (sendedMessageList.Count > 0)
            {
                foreach (var message in sendedMessageList)
                {
                    resultUser = new MessageListDto();
                    resultUser.UserId = message.RecipientId;
                    resultUser.IsSender = true;
                    resultUser.DateAdded = message.DateAdded;
                    resultUser.IsRead = message.IsRead;
                    resultUser.Text = message.Text;
                    result.Add(resultUser);

                }
            }
            if (receivedMessagelist.Count > 0)
            {
                foreach (var message in receivedMessagelist)
                {
                    resultUser = new MessageListDto();

                    resultUser.UserId = message.SenderId;
                    resultUser.IsSender = false;
                    resultUser.DateAdded = message.DateAdded;
                    resultUser.IsRead = message.IsRead;
                    resultUser.Text = message.Text;
                    result.Add(resultUser);
                }
            }

            var res = result.OrderByDescending(x => x.DateAdded).ToList(); ;
            return new SuccessDataResult<List<MessageListDto>>(res);


        }

        public List<UserListForMessageDto> GetMessageUserList(int CurrentUserId)
        {
            var messageList = GetMessageList(CurrentUserId).Data.DistinctBy(u => u.UserId).OrderByDescending(m => m.DateAdded);
            var user = new User();
            var userList = new List<User>();
            var resultUserList = new List<UserListForMessageDto>();
            foreach (var message in messageList)
            {
                user = new User();
                user = _userService.GetById(message.UserId);
                var result = _mapper.Map<UserListForMessageDto>(user);
                var usersChat = _messageDal.GetUsersChat(CurrentUserId, user.Id);
                if (usersChat != null) result.NewMessageCount = usersChat.Where(u => u.IsRead == false && u.RecipientId == CurrentUserId).Count();
                if (result.NewMessageCount > 0) { result.isNewMessage = true; }
                userList.Add(user);
                resultUserList.Add(result);

            }

            return resultUserList;
        }

        //Bu method;
        //1. Mesajlaşma sayfasında kullanıcıya tıklandığında
        //2. Kullanıcılar arasında mesajlaşma yapılırken mesaj gönderme işlemi sırasında çağrılmaktadır.
        //_messageDal.MessageIsRead methodu kullanıcıya tıklandığında o kullanıcıdan gelen mesajların okundu bilgisi işaretlenmek için hazırlanmıştır
        //Mesaj Gönderilme işlemi sırasında karşı tarafın mesajı okuyup okumadığı henüz bilinmediğinden "forCreateMessage" boolean bilgisi kullanılarak hangi işlem sırasında bu metodun çağrıldığı
        //tespit edilerek gelen mesajların okunma bilgisi set edilmektedir.
        public List<MessageListDto> GetUsersChat(int CurrentUserId, int FriendUserId, bool forCreateMessage)
        {
            var usersChat = _messageDal.GetUsersChat(CurrentUserId, FriendUserId);
            var messageList = new List<MessageListDto>();
            var message = new MessageListDto();
            if (usersChat != null)
            {
                foreach (var item in usersChat)
                {
                    var sender = _userService.GetById(item.SenderId);
                    var recipient = _userService.GetById(item.RecipientId);
                    if (forCreateMessage == false)
                    {
                        if (item.RecipientId == CurrentUserId)
                        {
                           
                                var isread = _messageDal.MessageIsRead(item);
                                message.IsRead = isread.IsRead;
                                message.DateRead = isread.DateRead;
                            
                        }
                    }
                    message = new MessageListDto();
                    message.Text = item.Text;
                    message.DateAdded = item.DateAdded;
                    message.UserId = item.SenderId;
                    message.SenderId = item.SenderId;
                    message.RecipientId = item.RecipientId;
                    message.ReceivedFirstName = recipient.FirstName;
                    message.ReceivedLastName = recipient.LastName;
                    message.SenderFirstName = sender.FirstName;
                    message.SenderLastName = sender.LastName;
                    message.SenderProfileImageURL = sender.ProfileImageURL;
                    message.ReceivedProfileImageURL = recipient.ProfileImageURL;

                    if (item.SenderId == CurrentUserId) message.IsSender = true;
                    messageList.Add(message);


                }

                return messageList;
            }
            return null;
        }

        public IResult UserExist(int userId)
        {
            var user = _userService.GetById(userId);
            if (user == null)
            {
                return new ErrorResult(Messages.UserNotFoundMessage);
            }
            return new SuccessResult();

        }

        public UsersConnectionIds SetUsersConnectionIds(UsersConnectionIds usersConnectionIds)
        {
            var result = _messageDal.SetUsersConnectionIds(usersConnectionIds);
            if (result != null) return result;
            return null;

        }

        public UsersConnectionIds GetUsersConnectionIds(int UserId)
        {
            var result = _messageDal.GetUserClient(UserId);
            if (result != null) return result;
            return null;
        }


    }
}
