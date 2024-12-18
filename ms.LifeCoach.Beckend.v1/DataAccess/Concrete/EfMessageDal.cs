using Core.DataAccess.EntityFramework;
using Core.Entities.Concrete;
using Core.Entities.Concrete.Dto;
using DataAccess.Abstract;
using DataAccess.Concrete.EntityFramework;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Concrete
{
    public class EfMessageDal : EfEntityRepositoryBase<Message, LifeCoachContext>, IMessageDal
    {
        public bool CreateMessage(Message message)
        {
            using (var context = new LifeCoachContext())
            {
                if (message != null)
                {
                    context.Add(message);
                    context.SaveChanges();
                    return true;
                }
                return false;
            }
        }



        public List<Message> GetReceivedMessageList(int CurrentUserId)
        {
            using (var context = new LifeCoachContext())
            {
                var messageList = context.Messages.Where(u => u.RecipientId == CurrentUserId).ToList();
                if (messageList != null) return messageList;

                return null;

            }
        }

        public List<Message> GetSendedMessageList(int CurrentUserId)
        {
            using (var context = new LifeCoachContext())
            {
                var messageList = context.Messages.Where(u => u.SenderId == CurrentUserId).ToList();
                if (messageList != null) return messageList;

                return null;

            }
        }

        public List<Message> GetUsersChat(int CurrentUserId, int FriendUserId)
        {

            using (var context = new LifeCoachContext())
            {
                var usersChat = context.Messages.Where(u => u.SenderId == CurrentUserId && u.RecipientId == FriendUserId
                                                       || u.SenderId == FriendUserId && u.RecipientId == CurrentUserId).ToList();
                if (usersChat != null) return usersChat.OrderByDescending(c => c.DateAdded).ToList();
                return null;
            }
        }

        public Message MessageIsRead(Message message)
        {
            using (var context = new LifeCoachContext())
            {
                message.IsRead = true;
                message.DateRead = DateTime.Now;
                context.Messages.Update(message);
                context.SaveChanges();
                return message;
            }
        }
        public UsersConnectionIds SetUsersConnectionIds(UsersConnectionIds usersConnectionIds)
        {
            using (var context = new LifeCoachContext())
            {
               
                var exist = context.UsersConnectionIds.Where(u => u.UserId == usersConnectionIds.UserId).FirstOrDefault();
       
                if (exist == null)
                {
                    context.Add(usersConnectionIds);
                    context.SaveChanges();
                    return usersConnectionIds;
                }
                else
                {
                    exist.IsConnected = usersConnectionIds.IsConnected;
                    exist.ConnectionId = usersConnectionIds.ConnectionId;
                    exist.ConnectedDate = DateTime.Now;
                    context.Update(exist);
                    context.SaveChanges();
                    return exist;
                }
            }

        }

        public UsersConnectionIds GetUserClient(int UserId)
        {
            using (var context = new LifeCoachContext())
            {
                var client = context.UsersConnectionIds.FirstOrDefault(u => u.UserId == UserId);
                if (client != null) return client;
                return null;
            }
        }
    }
}