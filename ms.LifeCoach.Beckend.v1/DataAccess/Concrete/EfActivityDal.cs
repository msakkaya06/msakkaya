using Core.DataAccess.EntityFramework;
using Core.Entities.Concrete;
using DataAccess.Abstract;
using DataAccess.Concrete.EntityFramework;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Activity = Entities.Concrete.Activity;

namespace DataAccess.Concrete
{
    public class EfActivityDal : EfEntityRepositoryBase<Activity, LifeCoachContext>, IActivityDal
    {
        public CommentActivities AddComment(CommentActivities comment)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Add(comment);
                context.SaveChanges();
                return comment;
            }
        }

        public Activity AddPost(int UserId, Activity activity)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Add(activity);
                context.SaveChanges();
                return activity;
            }
        }

        public List<CommentActivities> GetCommentsActivity(int activityId)
        {
            using (var context = new LifeCoachContext())
            {
                var res = context.CommentActivities.Where(a => a.ActivityId == activityId).ToList();
                return res;
            }
        }

        public List<Activity> GetFollowingUsersActivity(int userId)
        {
            using (var context = new LifeCoachContext())
            {
                var activities = new Activity();
                var result=new List<Activity>();
                var followings=context.UserToUsers.Where(f => f.FollowerId == userId && f.IsActive==true).Select(f => f.UserId).ToList();
                followings.Add(userId);//Ana sayfada gösterilecek gönderilere kullanıcının kendi gönderilerini de ekliyoruz.
                if (followings.Any())
                {
                    foreach (var user in followings)
                    {
                        activities = new Activity();
                        var ac = context.Activities.Where(a => a.UserId == user).ToList();
                        foreach (var activity in ac)
                        {
                            if (activity != null) result.Add(activity);

                        }
                       
                    }
                    return result;
                }
                return null;
            }
        }

        public List<Activity> GetUserActivity(int userId)
        {
            using (var context = new LifeCoachContext())
            {
                var res = context.Activities.Where(a => a.UserId == userId).ToList();
                return res;
            }
        }
    }
}
