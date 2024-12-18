using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class CreateCommentDto:IDto
    {

        public int UserId { get; set; }
   
        public int ActivityId { get; set; }
     
        public string? CommentText { get; set; }
    }
}
