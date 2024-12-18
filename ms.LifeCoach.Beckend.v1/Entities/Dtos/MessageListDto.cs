using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class MessageListDto
    {
        public int UserId { get; set; }
        public int SenderId { get; set; }
        public string SenderFirstName { get; set; }
        public string SenderLastName { get; set; }
        public string ReceivedFirstName { get; set; }
        public string ReceivedLastName { get; set; }
        public string SenderProfileImageURL { get; set; }
        public string ReceivedProfileImageURL { get; set; }
        public int RecipientId { get; set; }
        public bool IsSender { get; set; }
        public string Text { get; set; }
        public DateTime DateAdded { get; set; }
        public int CurrentUserId { get; set; }
        public int FriendUserId { get; set; }
        public int NewMessage { get; set; }
        public bool IsNewMessage { get; set; }
        public bool IsRead { get; set; }
        public DateTime? DateRead { get; set; }

    }
}
