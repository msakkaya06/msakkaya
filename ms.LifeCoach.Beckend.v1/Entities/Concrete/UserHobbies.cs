﻿using Core.Entities.Abstract;
using Core.Entities.Concrete;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Concrete
{
    public class UserHobbies:IEntity
    {
        public int Id { get; set; } 
        public User User { get; set; }  
        public Hobbies Hobbies { get; set; }
    }
}
