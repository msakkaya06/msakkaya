using Entities.Dtos;
using FluentValidation;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Business.Constants;

namespace Business.ValidationRules.FluentValidation
{
    public class UserValidator:AbstractValidator<UserForRegisterDto>
    {
        public UserValidator()
        {
            RuleFor(p=>p.Email).NotEmpty();
            RuleFor(p => p.Email).EmailAddress().WithMessage(Messages.ValidMessageEmail);
            RuleFor(p=>p.Password).NotEmpty();  
            RuleFor(p=>p.FirstName).NotEmpty(); 
            RuleFor(p=>p.LastName).NotEmpty();
            RuleFor(p=>p.BirthDay).NotEmpty();
            RuleFor(p => p.Password).MinimumLength(6).WithMessage(Messages.ValidMessagePassword);
          

        }
    }
}
