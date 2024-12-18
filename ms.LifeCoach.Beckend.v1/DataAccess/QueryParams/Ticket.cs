using DataAccess.Abstract;

namespace DataAccess.QueryParams
{
    public class Ticket:IQueryParams
    {
        public int Id { set; get; }
        public string Description { set; get; }
    }
}
