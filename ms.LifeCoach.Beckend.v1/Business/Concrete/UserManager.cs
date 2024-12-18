using AutoMapper;
using Business.Abstract;
using Business.BusinessAspects.Autofac;
using Business.Constants;
using CloudinaryDotNet.Actions;
using CloudinaryDotNet;
using Core.Aspects.Autofac.Logging;
using Core.CrossCuttingConcerns.Logging.Log4Net.Loggers;
using Core.Entities.Concrete;
using Core.Utilities.Results;
using DataAccess.Abstract;
using DataAccess.QueryParams;
using Entities.Dtos;
using Microsoft.IdentityModel.Tokens;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Business.DependencyResolvers.Helpers;
using Microsoft.Extensions.Configuration;
using DataAccess.Concrete;
using Core.Utilities.ConfigurationManager;

namespace Business.Concrete
{
    public class UserManager : IUserService
    {
        IUserDal _userDal;
        IMapper _mapper;
        public IConfiguration Configuration { get; }
        private Cloudinary _cloudinary;
        private CloudinarySettings _cloudinarySettings;


        public UserManager(IConfiguration configuration, IUserDal userDal, IMapper mapper)
        {
            _userDal = userDal;
            _mapper = mapper;
            Configuration = configuration;
            IConfiguration config = new ConfigurationBuilder()
            .AddJsonFile(GetConfigurationFile.GetBasePath())
            .Build();
            _cloudinarySettings = config.GetSection("CloudinarySettings").Get<CloudinarySettings>();
            Account account = new Account(
               _cloudinarySettings.CloudName,
               _cloudinarySettings.ApiKey,
               _cloudinarySettings.ApiSecret);

            _cloudinary = new Cloudinary(account);
            _cloudinary.Api.Secure = true;

        }

        public void Add(User user)
        {
            _userDal.Add(user);
        }

        //[SecuredOperation("User.List")]
        public List<UserListDto> GetAllUser()
        {
            var users = _userDal.GetAllUsers();
            var result = _mapper.Map<List<UserListDto>>(users);
            return result;

        }

        //[LogAspect(typeof(FileLogger))]
        public User GetByMail(string email)
        {
            return _userDal.Get(u => u.Email == email);
         
        }

        public User GetByUsername(string username)
        {
            return _userDal.Get(u => u.Username == username);
        }

        public User GetById(int userId)
        {
            return _userDal.Get(u => u.Id == userId);
        }

        public List<OperationClaim> GetClaims(User user)
        {
            return _userDal.GetClaims(user);
        }

        public UserListDto GetUser(string username, int userId)
        {
            var user = _userDal.Get(u => u.Username == username);
            var followCount = _userDal.GetFollowCount(user.Id);
            var result = _mapper.Map<User, UserListDto>(user);
            result.FollowersCount = followCount.FollowersCount;
            result.FollowingsCount=followCount.FollowingsCount; 
            var check = _userDal.IsFollowing(result.Id, userId);
            if (check) result.IsFollowing = true;
            if (!check) result.IsFollowing = false;

            return result;
        }

        public List<UserListDto> GetAllUserById(UserQueryParams queryParams)
        {
            var users = _userDal.GetAllUserById(queryParams);
            var result = _mapper.Map<List<UserListDto>>(users);
            if (!queryParams.Followers && !queryParams.Followings)
            {
                foreach (var user in result)
                {
                    var res = _userDal.IsFollowing(user.Id, queryParams.UserId);
                    if (res)
                    { user.IsFollowing = true; }
                    else
                    { user.IsFollowing = false; }

                }
            }
            return result;
        }

        public IResult IsAlreadyFollowed(int followeUserId, int userId)
        {
            var result = _userDal.IsAlreadyFollowed(followeUserId, userId);
            if (result)
                return new ErrorResult(Messages.IsAlreadyFollowed);
            return new SuccessResult();

        }

        public IDataResult<UserToUser> UserFollow(int followerUserId, int userId)
        {
            var result = _userDal.UserFollow(followerUserId, userId);
            if (result == null)
                return new ErrorDataResult<UserToUser>(Messages.ErrorUserFollowed);
            return new SuccessDataResult<UserToUser>(Messages.SuccessUserFollowed);

        }

        public IDataResult<User> UserProfileUpdate(UserListDto userProfile)
        {
            var user = GetByUsername(userProfile.Username);
            user.Educations = userProfile.Educations;
            user.WebSiteAdress = userProfile.WebSiteAdress;
            user.Username = userProfile.Username;
            user.Email = userProfile.Email;
            user.City = userProfile.City;
            user.Country = userProfile.Country;
            user.UpdatedDate = DateTime.Now;
            user.Introduction = userProfile.Introduction;
            user.Hobbies = userProfile.Hobbies;
            _userDal.Update(user);
            return new SuccessDataResult<User>(user, Messages.UserProfileUpdated);

        }

        public IResult UserUnfollow(int followeUserId, int userId)
        {
            var result = _userDal.UserUnfollow(followeUserId, userId);
            if (result)
                return new SuccessResult(Messages.SuccessUserUnfollowed);

            return new ErrorResult(Messages.ErrorUserUnfollowed);

        }

    }
}

