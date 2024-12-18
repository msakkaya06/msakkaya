using Core.DataAccess;
using Core.DataAccess.EntityFramework;
using Core.Entities.Concrete;
using Core.Utilities.Results;
using DataAccess.Abstract;
using DataAccess.Concrete.EntityFramework;
using DataAccess.QueryParams;
using Entities.Concrete;
using Entities.Dtos;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Concrete
{
    public class EfUserDal : EfEntityRepositoryBase<User, LifeCoachContext>, IUserDal
    {
   
        public List<User> GetAllUserById(UserQueryParams queryParams)
        {
            using (var context = new LifeCoachContext())
            {
                var users = context.Users
                    .Where(u => u.Id != queryParams.UserId)
                    .AsQueryable();



                if (queryParams.Followings)
                {
                    var result = GetFollows(queryParams.UserId, true);
                    users = users.Where(u => result.Contains(u.Id));

                }

                if (queryParams.Followers)
                {
                    var result = GetFollows(queryParams.UserId, false);
                    users = users.Where(u => result.Contains(u.Id));

                }
                return users.ToList();
            }
        }

        public List<User> GetAllUsers()
        {
            using (var context = new LifeCoachContext())
            {

                return context.Users.ToList();
            }
        }

        public List<OperationClaim> GetClaims(User user)
        {
            using (var context = new LifeCoachContext())
            {
                var result = from operationClaim in context.OperationClaims
                             join userOperationClaim in context.userOperationClaims
                             on operationClaim.Id equals userOperationClaim.OperationClaimId
                             where userOperationClaim.UserId == user.Id
                             select new OperationClaim { Id = userOperationClaim.Id, Name = operationClaim.Name };
                return result.ToList();
            }
        }

        public UserFollowCount GetFollowCount(int userId)
        {
            using (var context = new LifeCoachContext())
            {
                UserFollowCount result=new UserFollowCount();
                var followersCount = context.UserToUsers.Count(u => u.UserId == userId && u.IsActive == true);
                var followingsCount = context.UserToUsers.Count(u => u.FollowerId == userId && u.IsActive == true);
                result.FollowersCount = followersCount; 
                result.FollowingsCount = followingsCount;   
                return result;
            }
        }

        public string GetUserProfilePhoto(int UserId)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Users.Where(p => p.Id == UserId).FirstOrDefault().ProfileImageURL?.ToString();
                   
                return result;
            }
        }

        public bool IsAlreadyFollowed(int followerUserId, int userId)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.UserToUsers.Any(u => u.UserId == userId && u.FollowerId == followerUserId&& u.IsActive==true);
                return result;
            }

        }
        public bool IsFollowing(int followingUserId, int userId)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.UserToUsers.Any(u => u.UserId == followingUserId && u.FollowerId == userId && u.IsActive==true);
                return result;
            }
        }

        public UserToUser UserFollow(int followerUserId, int userId)
        {
            using (var context = new LifeCoachContext())
            {
                
                var firstCheck=context.UserToUsers.Where(c=>c.UserId== userId && c.FollowerId==followerUserId && c.IsActive==false).FirstOrDefault();
                if(firstCheck!=null)
                {
                    firstCheck.IsActive = true;
                    context.SaveChanges();
                    return firstCheck;
                }
                else
                {
                    var userToUser = new UserToUser()
                    {
                        FollowerId = followerUserId,
                        UserId = userId,
                        IsActive = true

                    };

                    var result = context.Add(userToUser);
                    context.SaveChanges();
                    return userToUser;
                }
            }
        }

        public bool UserUnfollow(int followerUserId, int userId)
        {
            using (var context = new LifeCoachContext())
            {
                var userToUser = context.UserToUsers.Where(u => u.FollowerId == followerUserId && u.UserId == userId && u.IsActive == true).FirstOrDefault();
                if (userToUser != null)
                {
                    userToUser.IsActive = false;
                    context.SaveChanges();
                    return true;

                }
                return false;
                    
            }
        }

        private IEnumerable<int> GetFollows(int userId, bool IsFollowings)
        {
            using (var context = new LifeCoachContext())
            {
                var user = context.Users
                                  .Include(i => i.Followers)
                                  .Include(i => i.Followings)
                                  .FirstOrDefault(i => i.Id == userId);
                if (IsFollowings)
                {
                    return user.Followers
                        .Where(i => i.FollowerId == userId && i.IsActive==true)
                        .Select(i => i.UserId);
                }
                else
                {
                    return user.Followings
                        .Where(i => i.UserId == userId && i.IsActive == true)
                        .Select(i => i.FollowerId);
                }
            }

        }

     
    }
}