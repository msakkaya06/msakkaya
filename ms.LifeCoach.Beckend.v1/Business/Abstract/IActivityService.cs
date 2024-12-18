using Core.Utilities.Results;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.Abstract
{
    public interface IActivityService
    {
        public List<ActivityPostListDto> GetFollowingUsersActivity(int userId);
        public List<ActivityPostListDto> GetUserActivity(int userId);
        public IDataResult<CommentActivities> AddComment(CreateCommentDto createCommentDto);

        public List<ReturnCommentActivityDto> GetCommentsActivity(int activityId);

        public IResult AddActivity(int userId,List<PhotoForActivity> photoForCreationDtoList);

    }
}
