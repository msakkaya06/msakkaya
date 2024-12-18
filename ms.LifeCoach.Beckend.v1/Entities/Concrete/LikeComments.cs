using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class LikeComments:IEntity
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public int CommentId { get; set; }

        public int CreatedDate { get; set; }

        public bool IsActive { get; set; }
    }
}
