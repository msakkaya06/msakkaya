using DataAccess.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.QueryParams
{
    public class UserQueryParams:IQueryParams
    {
        public int UserId { get; set; }
        public bool Followers { get; set; }
        public bool Followings { get; set; }
    }
}
