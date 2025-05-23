﻿using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Core.Entities.Concrete
{
    public class Message:IEntity
    {
        public int Id { get; set; }
        public int SenderId { get; set; }
        public User Sender { get; set; }

        public int RecipientId { get; set; }
        public User Recipient { get; set; }
        public string Text { get; set; }
        public DateTime DateAdded { get; set; }
        public DateTime? DateRead{ get; set; }
        public bool IsRead { get; set; } = false;
        public bool SenderDeleted{ get; set; }
        public bool RecipientDeleted{ get; set; }
    }
}
