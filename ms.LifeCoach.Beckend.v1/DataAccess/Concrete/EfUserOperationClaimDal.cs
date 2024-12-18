using Core.DataAccess.EntityFramework;
using Core.Entities.Concrete;
using DataAccess.Abstract;
using DataAccess.Concrete.EntityFramework;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DataAccess.Concrete
{
    public class EfUserOperationClaimDal:EfEntityRepositoryBase<UserOperationClaim,LifeCoachContext>,IUserOperationClaimDal
    {

    }
}
