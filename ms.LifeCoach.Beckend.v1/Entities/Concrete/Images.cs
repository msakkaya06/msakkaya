﻿using Core.Entities.Abstract;
using Core.Entities.Concrete;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class Images:IEntity
    {

        public int Id { get; set; }
        public int UserId { get; set; }
        public string Url { get; set; }
        public string? Description { get; set; }
        public DateTime DateAdded { get; set; }
        public bool IsMain { get; set; }
        public string PublicId { get; set; }
        public int? ActivityId { get; set; }
     

     
       


    }
}
