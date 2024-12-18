using Core.Entities.Concrete;
using Core.Utilities.Results;
using DataAccess.QueryParams;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.Abstract
{
    public interface IUserService
    {

        List<OperationClaim> GetClaims(User user);
        void Add(User user);
        User GetByMail(string email);
        User GetByUsername(string username);
        User GetById(int userId);
        List<UserListDto> GetAllUser();
        List<UserListDto> GetAllUserById(UserQueryParams queryParams);
        UserListDto GetUser(string username, int userId);

        IDataResult<User> UserProfileUpdate(UserListDto userProfile);  

        IResult IsAlreadyFollowed(int followeUserId, int userId);

        IDataResult<UserToUser> UserFollow(int followeUserId, int userId);

        IResult UserUnfollow(int followeUserId, int userId);

    }
}
