using Core.Entities.Concrete;
using Core.Utilities.ConfigurationManager;
using Entities.Concrete;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Concrete.EntityFramework
{
    public class LifeCoachContext : DbContext

    {
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            Initializer.Build();
            IConfiguration config = new ConfigurationBuilder()
           .AddJsonFile(GetConfigurationFile.GetBasePath())
           .Build();
            var data = config.GetConnectionString("SqlCon");
         
            //ms home
            optionsBuilder.UseSqlServer(@data.ToString());

            //ms business
            //Data Source=localhost;Initial Catalog=LifeCoachDb;Integrated Security=True;Connect Timeout=30;Encrypt=False;Trust Server Certificate=False;Application Intent=ReadWrite;Multi Subnet Failover=False
           //optionsBuilder.UseSqlServer(@"Data Source=localhost;Initial Catalog=LifeCoachDb;Integrated Security=True;Connect Timeout=30;Encrypt=False;TrustServerCertificate=False;ApplicationIntent=ReadWrite;MultiSubnetFailover=False");

        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<UserToUser>()
                .HasKey(k => new { k.UserId,k.FollowerId});

            modelBuilder.Entity<UserToUser>()
                .HasOne(l => l.User)
                .WithMany(a => a.Followers)
                .HasForeignKey(l => l.FollowerId);

            modelBuilder.Entity<UserToUser>()
             .HasOne(l => l.Follower)
             .WithMany(a => a.Followings)
             .HasForeignKey(l => l.UserId);


            modelBuilder.Entity<Message>()
                    .HasOne(i => i.Sender)
                    .WithMany(i => i.MessagesSent)
                    .HasForeignKey(i => i.SenderId);

            modelBuilder.Entity<Message>()
                .HasOne(i => i.Recipient)
                .WithMany(i => i.MessagesReceived)
                .HasForeignKey(i => i.RecipientId);


        }

        public DbSet<User> Users { get; set; }
        public DbSet<Location> Locations { get; set; }
        public DbSet<UserLocation> UserLocations { get; set; }
        public DbSet<Activity> Activities { get; set; }
        public DbSet<Images> Images { get; set; }
        public DbSet<LifeCoachMaster> LifeCoachMaster { get; set; }
        public DbSet<OperationClaim> OperationClaims { get; set; }
        public DbSet<UserOperationClaim> userOperationClaims { get; set; }
        public DbSet<Weather> Weathers { get; set; }
        public DbSet<Hobbies> Hobbies { get; set;}
        public DbSet<Country> Countries { get; set; }
        public DbSet<City> Cities { get; set; }
        public DbSet<UserHobbies> UserHobbies { get; set; } 
        public DbSet<UserToUser> UserToUsers { get; set; }  
        public DbSet<Message> Messages { get; set; }
        public DbSet<Photo> Photos { get; set; }    
        public DbSet<CommentActivities> CommentActivities { get; set; } 
        public DbSet<LikeActivities> LikeActivities { get; set; }
        public DbSet<LikeComments> LikeComments { get; set; }
        public DbSet<UsersConnectionIds> UsersConnectionIds { get; set; }

        




    }
}
