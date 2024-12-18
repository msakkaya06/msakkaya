using Azure.Core.Pipeline;
using Core.Entities.Abstract;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Entities.Dtos
{
    public class PhotoForActivity : IDto
    {
        public int Id { get; set; }
        public string? Url { get; set; }
        public bool? IsMain  { get; set; }
        public DateTime? DateAdded { get; set; }
        public string? Description { get; set; }
    }
}
