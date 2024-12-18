using Core.Entities.Abstract;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class UserImagesDto:IDto
    {
        public string Username { get; set; }
        public string Description { get; set; }
        public string ImageURL { get; set; }
        public DateTime CreatedDate { get; set; }
    }
}
