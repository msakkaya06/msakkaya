using System;
using System.Collections.Generic;
using System.Text;

namespace Core.CrossCuttingConcerns.Logging
{
    public class LogParameter
    {
        public string Name { get; set; }
        public object Value { get; set; }
        public string Type { get; set; }
        public int StatusCode { get; set; }
        public string Message { get; set; }
        public DateTime Date { get; set; }  
    }
}
