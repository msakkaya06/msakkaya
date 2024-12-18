using Core.Entities.Abstract;
using Entities.Concrete;
using Microsoft.Identity.Client;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class ActivityPostListDto : IDto
    {
        public int UserId { get; set; }
        public int ActivityId { get; set; }
        public string UserFirstName { get; set; }
        public string UserLastName { get; set; }
        public string Username { get; set; }
        public string? UserProfileImageUrl { get; set; }
        public string? Description { get; set; }

        public DateTime StartTime { get; set; }
        public int? CodeEnvironment { get; set; }
        public List<Images> Images { get; set; }
        public List<ReturnCommentActivityDto>? Comments { get; set; }
        public int CommentsCount { get; set; }

        public bool IsMultiPhoto { get; set; } = false;
    }
}