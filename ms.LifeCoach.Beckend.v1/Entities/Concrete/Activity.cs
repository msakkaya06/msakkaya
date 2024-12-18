using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class Activity:IEntity
    {
        public int Id { get; set; }
        public int UserId { get; set; }
        public string? Description { get; set; }
        public DateTime StartTime { get; set; }
        public DateTime? FinishTime { get; set; }
        public int? CodeEnvironment { get; set; }    
       
     
        public DateTime CreatedDate { get; set; }
        public DateTime? UpdatedDate { get; set; }
        public bool isActive { get; set; }
        //public LifeCoachMaster LifeCoachMaster { get; set; }


    }

}
