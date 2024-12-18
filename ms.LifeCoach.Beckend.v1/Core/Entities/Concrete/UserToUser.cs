using Core.Entities.Abstract;
using Core.Entities.Concrete;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Core.Entities.Concrete
{
    public class UserToUser:IEntity
    {
        public int UserId { get; set; }
        public User User { get; set; }

        public int FollowerId { get; set; }
        public User Follower { get; set; }  

        public bool? IsActive { get; set; }
    }
}
