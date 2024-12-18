using AutoMapper;
using Business.Abstract;
using Business.Extensions;
using Core.Entities.Concrete;
using Core.Entities.Concrete.Dto;
using Entities.Concrete;
using Entities.Dtos;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Business.DependencyResolvers
{
    public class MapperProfiles : Profile
    {
        public MapperProfiles()
        {
            CreateMap<User, UserForLoginDto>();
            CreateMap<User, UserForRegisterDto>();
            CreateMap<User, UserListDto>()
            .ForMember(dest => dest.Age, opt => opt.MapFrom(src => src.DateofBirth.CalculateAge()));
            CreateMap<User, UserListForMessageDto>();
            CreateMap<User, UserListForMessageDto>().ReverseMap();
            CreateMap<UserListDto, User>()
                    .ForMember(dest => dest.City, opt => opt.MapFrom(src => src.City))
                    .ForMember(dest => dest.Introduction, opt => opt.MapFrom(src => src.Introduction))
                    .ForMember(dest => dest.Country, opt => opt.MapFrom(src => src.Country))
                    .ForMember(dest => dest.Username, opt => opt.MapFrom(src => src.Username));
            CreateMap<Message, MessageForCreateDto>();
            CreateMap<Message, MessageForCreateDto>().ReverseMap();
            CreateMap<PhotoForCreationDto, Images>();
            CreateMap<PhotoForCreationDto, Images>().ReverseMap();
            CreateMap<PhotoForReturnDto, Images>();
            CreateMap<PhotoForReturnDto, Images>().ReverseMap();
            CreateMap<Activity, ActivityPostListDto>();
            CreateMap<Activity, ActivityPostListDto>().ReverseMap();
            CreateMap<CommentActivities, CreateCommentDto>();
            CreateMap<CommentActivities, CreateCommentDto>().ReverseMap();
            CreateMap<CommentActivities, ReturnCommentActivityDto>();
            CreateMap<CommentActivities, ReturnCommentActivityDto>().ReverseMap();
      

        }
    }
}
