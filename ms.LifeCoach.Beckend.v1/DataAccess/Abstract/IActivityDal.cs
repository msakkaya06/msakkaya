using Core.DataAccess;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Abstract
{
    public interface IActivityDal : IEntityRepository<Activity>
    {
        Activity AddPost(int UserId, Activity activity);
        public List<Activity> GetUserActivity(int userId);
        public List<Activity> GetFollowingUsersActivity(int userId);
        CommentActivities AddComment (CommentActivities comment);
        List<CommentActivities> GetCommentsActivity(int activityId);

    }
}
