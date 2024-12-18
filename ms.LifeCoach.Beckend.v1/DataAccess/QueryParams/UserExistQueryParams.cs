using DataAccess.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.QueryParams
{
    public class UserExistQueryParams:IQueryParams
    {
        public int UserId { get; set; }
        public string UserName { get; set; }
        public string EMail { get; set; }
    }
}
