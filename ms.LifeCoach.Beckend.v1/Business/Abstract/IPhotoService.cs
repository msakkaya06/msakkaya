using Core.Utilities.Results;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.Abstract
{
    public interface IPhotoService
    {
        PhotoForReturnDto AddProfilePhoto(int userId, PhotoForCreationDto photoForCreationDto);
        PhotoForReturnDto AddPost(int userId, PhotoForCreationDto photoForCreationDto);
        PhotoForReturnDto AddImage(int userId, PhotoForCreationDto photoForCreationDto);
    }
}
