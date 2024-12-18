using Core.Entities.Abstract;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Internal;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations.Schema;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class Location : IEntity
    {
        public int Id { get; set; }

        [Precision(8,6)]
        public decimal xKoordinat { get; set; }

        [Precision(9, 6)]
        public decimal yKoordinat { get; set; }

        public int CodeCountry { get; set; }
        public int CodeCity { get; set; }
        public DateTime CreatedDate { get; set; }
        public DateTime? UpdatedDate { get; set; }
        public bool Active { get; set; }
    }
}
