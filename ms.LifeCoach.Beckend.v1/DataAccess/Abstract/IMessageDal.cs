using Core.DataAccess;
using Core.Entities.Concrete;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Abstract
{
    public interface IMessageDal : IEntityRepository<Message>
    {

        bool CreateMessage(Message message);
        List<Message> GetSendedMessageList(int CurrentUserId);
        List<Message> GetReceivedMessageList(int CurrentUserId);
        List<Message> GetUsersChat(int CurrentUserId, int FriendUserId);
        public UsersConnectionIds SetUsersConnectionIds(UsersConnectionIds usersConnectionIds);
        public UsersConnectionIds GetUserClient(int UserId);
        public Message MessageIsRead(Message message);
    }
}
