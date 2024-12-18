using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Business.DependencyResolvers;
using Business.DependencyResolvers.Helpers;
using Business.DependencyResolvers.SignalR.HubConfig;
using Core.DependencyResolvers;
using Core.Extensions;
using Core.Utilities.ConfigurationManager;
using Core.Utilities.IoC;
using Core.Utilities.Security.Encyption;
using Core.Utilities.Security.Jwt;
using DataAccess.Concrete.EntityFramework;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.HttpsPolicy;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.IdentityModel.Tokens;
using WebAPI.Helpers;

namespace WebAPI
{
    public class Startup
    {
        public Startup(IConfiguration configuration)
        {
            Configuration = configuration;


        }

        public IConfiguration Configuration { get; }

        // This method gets called by the runtime. Use this method to add services to the container.
        public void ConfigureServices(IServiceCollection services)
        {
            IConfiguration config = new ConfigurationBuilder()
            .AddJsonFile(GetConfigurationFile.GetBasePath())
            .AddEnvironmentVariables()
.           Build();
            services.AddControllers().AddNewtonsoftJson();
            services.AddDependencyResolvers(new ICoreModule[]
          {
                new BusinessModule()
          });
            services.Configure<CloudinarySettings>(config.GetSection("CloudinarySettings"));
            services.AddCors(options =>
            {

                options.AddPolicy("AllowOrigin",
                    builder => builder.WithOrigins("http://localhost:4300"));
                options.AddPolicy("AllowOrigin",
                    builder => builder.WithOrigins("http://localhost:40000"));

            });

            var tokenOptions = config.GetSection("TokenOptions").Get<TokenOptions>();


            services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
                .AddJwtBearer(options =>
                {
                    options.TokenValidationParameters = new TokenValidationParameters
                    {
                        ValidateIssuer = true,
                        ValidateAudience = true,
                        ValidateLifetime = true,
                        ValidIssuer = tokenOptions.Issuer,
                        ValidAudience = tokenOptions.Audience,
                        ValidateIssuerSigningKey = true,
                        IssuerSigningKey = SecurityKeyHelper.CreateSecurityKey(tokenOptions.SecurityKey)
                    };
                });
            services.AddDependencyResolvers(new ICoreModule[]
           {
                new CoreModule(),
           });

            services.AddScoped<LastActiveActionFilter>();
        }

        // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
        public void Configure(IApplicationBuilder app, IWebHostEnvironment env)
        {
            if (env.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }
            app.ConfigureCustomExceptionMiddleware();


            app.UseHttpsRedirection();

            app.UseRouting();
            app.UseCors(builder => builder.WithOrigins("http://localhost:4300").AllowAnyHeader().AllowAnyMethod().AllowCredentials());


            app.UseAuthentication();

            app.UseAuthorization();
            app.UseEndpoints(endpoints =>
            {
                endpoints.MapControllers();
                endpoints.MapHub<ChatHub>("/userschat");
            });


        }
    }
}
