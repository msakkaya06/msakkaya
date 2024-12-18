using Core.DataAccess.EntityFramework;
using Core.Entities.Concrete;
using DataAccess.Abstract;
using DataAccess.Concrete.EntityFramework;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Concrete
{
    public class EfImagesDal : EfEntityRepositoryBase<Images, LifeCoachContext>, IImagesDal
    {
        public bool AddPhoto(int userId, Images images)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Add(images);
                context.SaveChanges();
                return true;
            }
        }

 

        public List<Images> GetPhotosForActivity(int ActivityId)
        {
            using (var context = new LifeCoachContext())
            {
                var result=context.Images.Where(i=>i.ActivityId == ActivityId).ToList();    
                return result;
            }
        }

        public bool UpdateProfilePhoto(int userId, Images images)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Update(images);
                context.SaveChanges();
                return true;
            }
        }

        public Images GetPhoto(int photoId)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Images.Where(i=>i.Id== photoId).FirstOrDefault();
                return result;
            }
        }

        public Images UpdatePhoto(Images photo)
        {
            using (var context = new LifeCoachContext())
            {
                var result = context.Update(photo);
                context.SaveChanges();
                return photo;
            }
        }
    }
}
