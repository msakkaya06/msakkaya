using AutoMapper;
using Business.Abstract;
using CloudinaryDotNet.Actions;
using CloudinaryDotNet;
using Core.Aspects.Autofac.Caching;
using Core.Aspects.Autofac.Performance;
using Core.Aspects.Autofac.Transaction;
using Core.Utilities.Results;
using DataAccess.Abstract;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Core.Entities.Concrete;
using Business.Constants;

namespace Business.Concrete
{
    public class ActivityManager : IActivityService
    {
        public IImagesDal _imagesDal;
        public IActivityDal _activityDal;
        IUserDal _userDal;
        IMapper _mapper;
        public ActivityManager(IImagesDal imagesDal, IActivityDal activityDal, IUserDal userDal, IMapper mapper)
        {
            _imagesDal = imagesDal;
            _activityDal = activityDal;
            _userDal = userDal;
            _mapper = mapper;
        }


        [TransactionScopeAspect]
        [PerformanceAspect(1)]
        public IResult AddActivity(int userId,List<PhotoForActivity> photoForCreationDtoList)
        {
            var activity = new Activity();
            activity.StartTime = DateTime.Now;
            activity.CreatedDate = DateTime.Now;
            activity.Description = photoForCreationDtoList[0].Description;
            activity.isActive = true;
            activity.UserId = userId;
            var result=_activityDal.AddPost(userId,activity); 
            foreach (var photo in photoForCreationDtoList)
            {
                var photoDto = new PhotoForActivity();
                var image = _imagesDal.GetPhoto(photo.Id);
                image.ActivityId = result.Id;
                var update = _imagesDal.UpdatePhoto(image);
            }
            if(result!=null) { return new SuccessResult(Messages.SuccessCreatedActivity); }
            return new ErrorResult(Messages.ErrorCreatedActivity);  
               
            }
           
        

        public IDataResult<CommentActivities> AddComment(CreateCommentDto createCommentDto)
        {
            var comment = _mapper.Map<CommentActivities>(createCommentDto);
            comment.IsActive = true;
            comment.CreatedDate = DateTime.Now;
            var result = _activityDal.AddComment(comment);
            if (result != null) { return new SuccessDataResult<CommentActivities>(result); }
            return new ErrorDataResult<CommentActivities>();
        }

        public List<ReturnCommentActivityDto> GetCommentsActivity(int activityId)
        {
            var comments = _activityDal.GetCommentsActivity(activityId);
            var result = new List<ReturnCommentActivityDto>();
            var res = new ReturnCommentActivityDto();
            if(comments != null)
            {
                foreach (var comment in comments)
                {
                    res = new ReturnCommentActivityDto();
                    var user = _userDal.Get(u => u.Id == comment.UserId);
                    res = _mapper.Map<ReturnCommentActivityDto>(comment);
                    if (user != null)
                    {
                        res.UserFirstName = user.FirstName;
                        res.UserLastName = user.LastName;
                        res.Username = user.Username;
                        res.UserProfileImageUrl = user.ProfileImageURL;
                    }
                    result.Add(res);
                }
                return result;
            }
            return null;          
        }

        [PerformanceAspect(1)]
        public List<ActivityPostListDto> GetFollowingUsersActivity(int userId)
        {
            var activities = _activityDal.GetFollowingUsersActivity(userId);
            var result = GetActivities(activities);
            return result;
        }

        public List<ActivityPostListDto> GetUserActivity(int userId)
        {
            var activities = _activityDal.GetUserActivity(userId);
            var result = GetActivities(activities);
            return result;
        }




        private List<ActivityPostListDto> GetActivities(List<Activity> activities)
        {
            var resultList = new List<ActivityPostListDto>();
            var res = new ActivityPostListDto();
            res.Images = new List<Images>();
            if (activities != null)
            {
                
                foreach (var activity in activities)
                {
                    res = new ActivityPostListDto();
                    var images = _imagesDal.GetPhotosForActivity(activity.Id);
                    var user = _userDal.Get(u => u.Id == activity.UserId);
                    var comments=GetCommentsActivity(activity.Id);
                    res = _mapper.Map<ActivityPostListDto>(activity);
                    res.ActivityId = activity.Id;
                    res.UserFirstName = user.FirstName;
                    res.UserLastName = user.LastName;
                    res.Username = user.Username;
                    res.UserProfileImageUrl = _userDal.GetUserProfilePhoto(activity.UserId);
                    res.CommentsCount = 0;
                    if (comments != null)
                    {
                        res.CommentsCount = comments.Count;
                        res.Comments = new List<ReturnCommentActivityDto>();
                        foreach (var comment in comments)
                        {
                            res.Comments.Add(comment);
                        }
                    }
                 
                    if (images != null)
                    {
                        res.Images = new List<Images>();
                        foreach (var image in images)
                        {
                            res.Images.Add(image);
                        }
                    }

                    if(images.Count >1)
                    {
                        res.IsMultiPhoto = true;
                    }
                    resultList.Add(res);
                }
                return resultList.OrderByDescending(p => p.StartTime).ToList();
            }
            return null;
        }
    }
}
