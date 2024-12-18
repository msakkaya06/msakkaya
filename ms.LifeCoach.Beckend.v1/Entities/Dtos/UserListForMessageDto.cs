using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class UserListForMessageDto
    {
        public int Id { get; set; }
        public string Email { get; set; }
        public string Username { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public DateTime? LastActive { get; set; }
        public string? ProfileImageURL { get; set; }
        public int NewMessageCount { get; set; }
        public bool isNewMessage { get; set; }

    }
}
