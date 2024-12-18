using Core.Entities.Concrete;
using Core.Entities.Concrete.Dto;
using Core.Utilities.Results;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.Abstract
{

    public interface IMessageService
    {
        IResult UserExist(int userId);

        IDataResult<MessageForCreateDto> CreateMessage(MessageForCreateDto messageForCreateDto);

        IDataResult<List<MessageListDto>> GetMessageList(int CurrentUserId);

        List<UserListForMessageDto> GetMessageUserList (int CurrentUserId);
        List<MessageListDto> GetUsersChat(int CurrentUserId, int FriendUserId, bool forCreateMessage);
        public UsersConnectionIds SetUsersConnectionIds(UsersConnectionIds usersConnectionIds);
        public UsersConnectionIds GetUsersConnectionIds(int UserId);



    }
}
