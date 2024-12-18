using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class Weather:IEntity
    {
        public int Id { get; set; }
        public int Degree { get; set; }

        public string? Status { get; set; }
        public int CodeCity { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime? UpdatedDate { get; set; }
        public bool Active { get; set; }

    }
}




