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
    public interface IImagesDal:IEntityRepository<Images>
    {

        bool AddPhoto(int userId, Images images);
        bool UpdateProfilePhoto(int userId, Images images);
        public Images GetPhoto(int photoId);

        public Images UpdatePhoto(Images photo);
        public List<Images> GetPhotosForActivity(int ActivityId);
    }
}
