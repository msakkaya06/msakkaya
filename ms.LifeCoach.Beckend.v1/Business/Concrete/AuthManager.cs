using Business.Abstract;
using Core.Entities.Concrete;
using Core.Utilities.Results;
using Core.Utilities.Security.Hashing;
using Core.Utilities.Security.Jwt;
using Entities.Dtos;
using Entities.Concrete;
using Business.Constants;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.ComponentModel.DataAnnotations;
using Business.ValidationRules.FluentValidation;
using Core.Aspects.Autofac.Validation;
using AutoMapper;
using DataAccess.QueryParams;
using Core.Aspects.Autofac.Logging;
using Core.CrossCuttingConcerns.Logging.Log4Net.Loggers;

namespace Business.Concrete
{
    public class AuthManager : IAuthService
    {

        private IUserService _userService;
        private ITokenHelper _tokenHelper;
        private IMapper _mapper;




        public AuthManager(IUserService userService, ITokenHelper tokenHelper, IMapper mapper)
        {
            _userService = userService;
            _tokenHelper = tokenHelper;
            _mapper=mapper;
        }
        public IDataResult<AccessToken> CreateAccessToken(User user)
        {
            var claims = _userService.GetClaims(user);
            var accessToken = _tokenHelper.CreateToken(user, claims);
            return new SuccessDataResult<AccessToken>(accessToken, Messages.AccessTokenCreated);
        }


        [LogAspect(typeof(DatabaseLogger))]
        public IDataResult<User> Login(UserForLoginDto userForLoginDto)
        {
            var userToCheck = _userService.GetByMail(userForLoginDto.Email);
            var usernameToCheck = _userService.GetByUsername(userForLoginDto.Email);
            if (userToCheck == null && usernameToCheck ==null)
            {
                return new ErrorDataResult<User>(Messages.UserNotFound);
            }

          
            if (userToCheck != null)
            {
                if (!HashingHelper.VerifyPasswordHash(userForLoginDto.Password, userToCheck.PasswordHash, userToCheck.PasswordSalt))
                {
                    return new ErrorDataResult<User>(Messages.PasswordError);
                }
                return new SuccessDataResult<User>(userToCheck, Messages.SuccessfulLogin); }
            if (usernameToCheck != null)
            {
                if (!HashingHelper.VerifyPasswordHash(userForLoginDto.Password, usernameToCheck.PasswordHash, usernameToCheck.PasswordSalt))
                {
                    return new ErrorDataResult<User>(Messages.PasswordError);
                }
                return new SuccessDataResult<User>(usernameToCheck, Messages.SuccessfulLogin);
            }
            return new ErrorDataResult<User>(Messages.UserNotFound);
        }
           
        
        [ValidationAspect(typeof(UserValidator),Priority =1)]
        public IDataResult<User> Register(UserForRegisterDto userForRegisterDto, string password)
        {
            byte[] passwordHash, passwordSalt;
            HashingHelper.CreatePasswordHash(password, out passwordHash, out passwordSalt);
            var user = new User
            {
                Email = userForRegisterDto.Email,
                Username=userForRegisterDto.Username,
                FirstName = userForRegisterDto.FirstName,
                LastName = userForRegisterDto.LastName,
                PasswordHash = passwordHash,
                PasswordSalt = passwordSalt,
                CreatedDate = DateTime.Now,
                DateofBirth=userForRegisterDto.BirthDay,
                Active = true
            };
            _userService.Add(user);
            return new SuccessDataResult<User>(user, Messages.UserRegistered);
        }

        public IResult UserExists(UserExistQueryParams userExistQueryParams)
        {
            if (_userService.GetByMail(userExistQueryParams.EMail) != null)
            {
                return new ErrorResult(Messages.UserAlreadyExists);
            }
            if(_userService.GetByUsername(userExistQueryParams.UserName) != null)
            { return new ErrorResult(Messages.UserAlreadyExists); }
            return new SuccessResult();
        }
    }
}
