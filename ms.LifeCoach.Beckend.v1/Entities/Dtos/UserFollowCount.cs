using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class UserFollowCount:IDto
    {
        public int FollowersCount { get; set; }
        public int FollowingsCount { get; set; }
    }
}
