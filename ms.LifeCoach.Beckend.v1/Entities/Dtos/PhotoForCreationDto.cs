using Core.Entities.Abstract;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class PhotoForCreationDto:IDto
    {
        public PhotoForCreationDto()
        {
            DateAdded = DateTime.Now;
        }
        public int Id { get; set; }
        public int UserId { get; set; }
        public string? Url { get; set; }
        public IFormFile File { get; set; }
        public string? Description { get; set; }
        public DateTime DateAdded { get; set; }
        public string? PublicId { get; set; }

    }
}
