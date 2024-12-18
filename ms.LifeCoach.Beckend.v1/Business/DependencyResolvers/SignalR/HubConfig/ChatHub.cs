using AutoMapper;
using Business.Abstract;
using Core.Aspects.Autofac.Exception;
using Core.CrossCuttingConcerns.Logging.Log4Net.Loggers;
using Core.Entities.Concrete;
using Core.Entities.Concrete.Dto;
using DataAccess.Abstract;
using Entities.Dtos;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.SignalR;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Core.Entities.Concrete.Dto;

namespace Business.DependencyResolvers.SignalR.HubConfig
{
    
    public class ChatHub : Hub
    {
        IMessageDal messageDal;
        IMessageService _messageService;
        IHubContext<ChatHub> _context;
        IHubCallerClients _callerClients;
        IMapper _mapper;

        public ChatHub(IMessageService messageService, IMapper mapper)
        {
            _messageService = messageService;
            _mapper = mapper;
        }
        public async Task BroadcastChartData(List<Message> data)
        {
            await Clients.All.SendAsync("broadcastuserschat", data);

        }
        public override async Task OnConnectedAsync()
        {     
            await Clients.Caller.SendAsync("userJoined", Context.ConnectionId.ToString());
        }
        
        [ExceptionLogAspect(typeof(FileLogger))]
        public async Task UserJoinedBusiness(UsersConnectionIds usersConnectionIds)
        {
            usersConnectionIds.ConnectedDate = DateTime.Now;
            usersConnectionIds.IsConnected = true;
           
            var result = _messageService.SetUsersConnectionIds(usersConnectionIds);
        }
        public async Task UserLeavedBusiness(UsersConnectionIds usersConnectionIds)
        {

            usersConnectionIds.IsConnected = false;

            var result = _messageService.SetUsersConnectionIds(usersConnectionIds);
        }

        public override async Task OnDisconnectedAsync(Exception exception)
        {
            UsersConnectionIds usersConnectionIds = new UsersConnectionIds();
            usersConnectionIds.ConnectionId = Context.ConnectionId.ToString();
            await Clients.Caller.SendAsync("userLeaved", Context.ConnectionId.ToString());
        }
        public async Task GetUsersChatRTT(GetUsersChatParamsDto messageListDto)
        {
            var usersChat = _messageService.GetUsersChat(messageListDto.CurrentUserId, messageListDto.FriendUserId, true);
            await Clients.All.SendAsync("broadcastuserschat", usersChat);
        }

        //CreateMessageRT fonksiyonu SignalR kullanarak mesaj oluşturmak için kullanılan fonksiyon.
        //Fonksiyonda gönderici ve alıcı kullanıcı ıdleri front-end tarafından parametre olarak alınır, kullanıcılar var mı kontrolü yapıldıktan sonra mesaj veri tabanına kaydedilir. 
        //Mesaj kaydı veri tabanına kaydedildikten sonra SignalR gönderimi için alıcı ve gönderici arasında ConnectionId üzerinden iletişim kurulur.
        //ConnectionIdler veri tabanında UserConnectionId tablosundan kontrol edilir. Kullanıcıların connectionId bilgisi varsa socket iletişim sağlanır yok ise kullanıcı daha sonra giriş yaptığında
        //veri tabanı üzerinden gelen mesajlarını kontrol eder.

        [ExceptionLogAspect(typeof (FileLogger))]   
        public async Task CreateMessageRT(MessageForCreateDto messageForCreateDto)
        {
           
            MessageListDto messageListDto = new MessageListDto();
            
            var recipient = _messageService.UserExist(messageForCreateDto.RecipientId);
            var sender = _messageService.UserExist(messageForCreateDto.SenderId);
            if (sender.Success && recipient.Success)
            {
                var client = _messageService.GetUsersConnectionIds(messageForCreateDto.RecipientId);
                var currentClient = _messageService.GetUsersConnectionIds(messageForCreateDto.SenderId);
                var message = _messageService.CreateMessage(messageForCreateDto);
                var usersChat = _messageService.GetUsersChat(messageForCreateDto.SenderId, messageForCreateDto.RecipientId, true);
                var receivedUserChat = _messageService.GetUsersChat(messageForCreateDto.RecipientId, messageForCreateDto.SenderId,true);
               if(currentClient!=null) await Clients.Client(currentClient.ConnectionId.ToString()).SendAsync("broadcastuserschat", usersChat);
             
                if(client!=null)await Clients.Client(client.ConnectionId.ToString()).SendAsync("broadcastuserschat", receivedUserChat);
            }
        }
    }
}
