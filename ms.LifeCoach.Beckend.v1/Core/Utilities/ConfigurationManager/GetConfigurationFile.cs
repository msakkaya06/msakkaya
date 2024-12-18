using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

namespace Core.Utilities.ConfigurationManager
{
    public static class GetConfigurationFile
    {

        public static string GetBasePath()
        {
            var relativePath = @"../DataAccess";
            var absolutePath = System.IO.Path.GetFullPath(relativePath);
            return absolutePath + "\\appsettings.json"; 
        }

      
    }
}
