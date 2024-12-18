using Core.DataAccess;
using Core.Entities.Concrete;
using Core.Utilities.Results;
using DataAccess.QueryParams;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Abstract
{
    public interface IUserDal:IEntityRepository<User>
    {
        List<OperationClaim> GetClaims(User user);
        List<User> GetAllUsers();
        List<User> GetAllUserById(UserQueryParams queryParams);
        bool IsAlreadyFollowed(int followerUserId, int userId);
        
        UserToUser UserFollow(int followerUserId, int userId);

        bool IsFollowing(int followingUserId, int userId);

        bool UserUnfollow(int followerUserId, int userId);
        string GetUserProfilePhoto(int UserId);

        UserFollowCount GetFollowCount(int userId);
      



        

      
    }
}
