using Core.Entities.Abstract;
using Core.Entities.Concrete;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class UserLocation:IEntity
    {
        public int Id { get; set; }
        public int UserId { get; set; }

        public int LocationId { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime? UpdatedDate { get; set; }
        public bool Active { get; set; }

        public Location Location { get; set; }  
        public User User { get; set; }




    }
}
