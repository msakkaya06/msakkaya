using Core.Entities.Abstract;

using Microsoft.Identity.Client;
using System;
using System.Collections.Generic;
using System.Text;
using System.Xml.Linq;

namespace Core.Entities.Concrete
{
    public class User:IEntity   
    {
        public int Id { get; set; }
        public string Username { get; set; }
        public string FirstName { get; set; }
        public string LastName { get; set; }
        public string Email { get; set; }
        public string? WebSiteAdress { get; set; }
        public string? Educations { get; set; }
        public string? Gender { get; set; }  
        public string? City { get; set; }
        public string? Country { get; set; }
        public DateTime DateofBirth { get; set; }
        public string? ProfileImageURL { get; set; }    
        public byte[] PasswordSalt { get; set; }
        public byte[] PasswordHash { get; set; }
        public string? Introduction { get; set; }
        public string? Hobbies { get; set; }
        public DateTime CreatedDate { get; set; }   
        public DateTime? UpdatedDate { get; set; }  
        public DateTime? LastActive { get; set; }
        public bool Active { get; set; }  
        
        public ICollection<UserToUser> Followings { get; set; }
        public ICollection<UserToUser> Followers { get; set; }    

        public ICollection<Message> MessagesSent { get; set; }
        
        public ICollection<Message> MessagesReceived { get; set; }  

        //public List<LifeCoachMaster> LifeCoachMasters { get;set; }=new List<LifeCoachMaster>(); 

       


    }
}
