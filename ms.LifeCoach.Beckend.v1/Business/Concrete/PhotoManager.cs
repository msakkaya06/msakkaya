using AutoMapper;
using Business.Abstract;
using Business.DependencyResolvers.Helpers;
using CloudinaryDotNet;
using CloudinaryDotNet.Actions;
using Core.Aspects.Autofac.Caching;
using Core.Aspects.Autofac.Exception;
using Core.Aspects.Autofac.Logging;
using Core.Aspects.Autofac.Performance;
using Core.Aspects.Autofac.Transaction;
using Core.CrossCuttingConcerns.Logging.Log4Net.Loggers;
using Core.Utilities.ConfigurationManager;
using Core.Utilities.Results;
using DataAccess.Abstract;
using Entities.Concrete;
using Entities.Dtos;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Options;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.Concrete
{
    public class PhotoManager : IPhotoService
    {
        private IUserService _userService;
        private IMapper _mapper;
        IImagesDal _imagesDal;
        IUserDal _userDal;
        IActivityDal _activityDal;
        public IConfiguration Configuration { get; }
        private Cloudinary _cloudinary;
        private CloudinarySettings _cloudinarySettings;
        public PhotoManager(IConfiguration configuration, IMapper mapper, IUserService userService, IImagesDal imagesDal, IUserDal userDal, IActivityDal activityDal)
        {
            _activityDal = activityDal;
            _userDal = userDal;
            _userService = userService;
            _mapper = mapper;
            Configuration = configuration;
            _imagesDal = imagesDal;
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

        [LogAspect(typeof(FileLogger))]   
        [PerformanceAspect(1)]
        public PhotoForReturnDto? AddProfilePhoto(int userId, PhotoForCreationDto photoForCreationDto)
        {
            var user = _userService.GetById(userId);
            if (user == null)
            {
                return null;
            }
            var file = photoForCreationDto.File;
            photoForCreationDto.UserId = user.Id;
            var uploadResult = new ImageUploadResult();
            if (file.Length > 0)
            {
                using (var stream = file.OpenReadStream())
                {
                    var uploadParams = new ImageUploadParams

                    {
                        File = new FileDescription(file.FileName, stream)
                    };

                    uploadResult = _cloudinary.Upload(uploadParams);
                }
            }
            var profilePhotoUrl = _cloudinary.Api.UrlImgUp.Transform(new Transformation().Height(210).Width(210)
                                 .Crop("scale"))
                                 .BuildUrl(uploadResult.PublicId + "." + uploadResult.Format);
            user.ProfileImageURL = profilePhotoUrl;
            photoForCreationDto.Url = uploadResult.Uri.ToString();
            photoForCreationDto.PublicId = uploadResult.PublicId;
            _userDal.Update(user);
            var photo = _mapper.Map<Images>(photoForCreationDto);
            var photoToReturn = _mapper.Map<PhotoForReturnDto>(photo);
            var result = _imagesDal.AddPhoto(userId, photo);
            if (result) return photoToReturn;
            return null;
        }
        [TransactionScopeAspect]
        [PerformanceAspect(1)]
        public PhotoForReturnDto? AddPost(int userId, PhotoForCreationDto photoForCreationDto)
        {
            var user = _userService.GetById(userId);
            var image = new Images();
            var activity = new Activity();
            if (user == null)
            {
                return null;
            }
            var file = photoForCreationDto.File;
            photoForCreationDto.UserId = user.Id;
            var uploadResult = new ImageUploadResult();
            if (file.Length > 0)
            {
                using (var stream = file.OpenReadStream())
                {
                    var uploadParams = new ImageUploadParams

                    {
                        File = new FileDescription(file.FileName, stream)
                    };
                    uploadResult = _cloudinary.Upload(uploadParams);

                }
            }
            activity.StartTime = DateTime.Now;
            activity.CreatedDate = DateTime.Now;
            activity.Description = photoForCreationDto.Description;
            activity.isActive = true;
            activity.UserId = user.Id;
            var activityRes=_activityDal.AddPost(userId, activity);
            image.Description = photoForCreationDto.Description;
            image.Url = uploadResult.Uri.ToString();
            image.DateAdded = DateTime.Now;
            image.UserId = user.Id;
            image.ActivityId= activityRes.Id;
            image.PublicId = uploadResult.PublicId;
            var result=_imagesDal.AddPhoto(userId,image);
            var photoToReturn = _mapper.Map<PhotoForReturnDto>(image);
            if (result) return photoToReturn;
            return null;
        }

        public PhotoForReturnDto AddImage(int userId, PhotoForCreationDto photoForCreationDto)
        {
            var user = _userService.GetById(userId);
            var image = new Images();
            var activity = new Activity();
            if (user == null)
            {
                return null;
            }
            var file = photoForCreationDto.File;
            photoForCreationDto.UserId = user.Id;
            var uploadResult = new ImageUploadResult();
            if (file.Length > 0)
            {
                using (var stream = file.OpenReadStream())
                {
                    var uploadParams = new ImageUploadParams

                    {
                        File = new FileDescription(file.FileName, stream)
                    };
                    uploadResult = _cloudinary.Upload(uploadParams);

                }
            }
            image.Description = photoForCreationDto.Description;
            image.Url = uploadResult.Uri.ToString();
            image.DateAdded = DateTime.Now;
            image.UserId = user.Id;
            image.PublicId = uploadResult.PublicId;
            var result = _imagesDal.AddPhoto(userId, image);
            var photoToReturn = _mapper.Map<PhotoForReturnDto>(image);
            if (result) return photoToReturn;
            return null;
        }
    }
}
