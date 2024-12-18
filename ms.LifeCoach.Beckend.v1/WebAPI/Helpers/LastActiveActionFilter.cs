using Microsoft.AspNetCore.Mvc.Filters;
using System.Security.Claims;

namespace WebAPI.Helpers
{
    public class LastActiveActionFilter : IAsyncActionFilter
    {
        public async Task OnActionExecutionAsync(ActionExecutingContext context, ActionExecutionDelegate next)
        {
            var resultContext= await next();
            var email= resultContext.HttpContext.User.FindFirst(ClaimTypes.NameIdentifier).Value;

        }
    }
}
