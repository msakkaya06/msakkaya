
using Business.Concrete;
using Business.DependencyResolvers.Helpers;
using Business.DependencyResolvers.RabbitMQ;
using Core.Utilities.IoC;
using Core.Utilities.RealTimeChat.SignalR;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.DependencyResolvers
{
    public class BusinessModule : ICoreModule
    {
        public void Load(IServiceCollection services)
        {
            services.AddAutoMapper(typeof(UserManager));
            services.AddAutoMapper(typeof(AuthManager));
            services.AddAutoMapper(typeof(MessageManager));
            services.AddAutoMapper(typeof(PhotoManager));

            services.AddSignalR();
            services.AddSingleton<TimerManager>();
            services.AddSingleton<RabbitMQHelper>();   
            services.AddSingleton<MailHelper>();
            services.AddSingleton<PasswordResetRequestHandler>();



        }
    }
}
