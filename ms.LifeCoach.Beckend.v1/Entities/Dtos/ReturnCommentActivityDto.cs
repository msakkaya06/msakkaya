using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class ReturnCommentActivityDto:IDto
    {
        public string UserFirstName { get; set; }
        public string UserLastName { get; set; }
        public string Username { get; set; }
        public int UserId { get; set; }
        public string CommentText { get; set; }
        public string? UserProfileImageUrl { get; set; }
        public DateTime CreatedDate { get; set; }

       
    }
}
