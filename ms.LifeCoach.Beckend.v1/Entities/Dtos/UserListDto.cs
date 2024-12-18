using System;
using System.Collections.Generic;
using System.Drawing;
using System.Text;
using Core.Entities.Abstract;

namespace Entities.Dtos
{
    public class UserListDto : IDto
    {
        public int Id { get; set; } 
        public string Email { get; set; }
        public string Username { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public int? Age { get; set; }
        public string? WebSiteAdress { get; set; }
        public string? Educations { get; set; }
        public string? Gender { get; set; }  
        public string? City { get; set; }    
        public string? Country { get; set; } 
        public DateTime? LastActive { get; set; }
        public Image? Image { get; set; }    
        public string? Hobbies { get; set; } 
        public int FollowingsCount { get; set; }
        public int FollowersCount { get; set; } 
        public string? ProfileImageURL { get; set; }   
        public string? Introduction { get; set; }
        public bool IsFollowing { get; set; }   



  
    }
}
