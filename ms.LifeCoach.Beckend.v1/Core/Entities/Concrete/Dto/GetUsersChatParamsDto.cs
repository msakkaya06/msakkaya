using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Core.Entities.Concrete.Dto
{
    public class GetUsersChatParamsDto:IDto
    {
        public int CurrentUserId { get; set; }
        public int FriendUserId { get; set; }
    }
}
