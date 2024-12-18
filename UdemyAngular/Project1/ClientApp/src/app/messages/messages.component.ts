import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { GetMessageParams, Message, MessageList } from '../_models/message';
import { User } from '../_models/user';

import { AlertifyService } from '../_services/alertify.service';
import { AuthService } from '../_services/auth.service';
import { MessageService } from '../_services/message.service';
import { SignalrService } from '../_services/signalr.service';

@Component({
  selector: 'messages',
  templateUrl: './messages.component.html',
  styleUrls: ['./messages.component.css']
})
export class MessagesComponent implements OnInit {

  constructor(public authService: AuthService,
    public messageService: MessageService,
    private router: Router,
    private alertify: AlertifyService,
    public signalrService: SignalrService) { }
  messages: MessageList[];
  sendMessages: MessageList[];
  users: User[];
  username: string;
  recipientId: number;
  messageText: string = '';
  params: GetMessageParams;

  message: Message;
  ngOnInit(): void {
    this.getMessageUserList(this.authService.decodedToken.NameId);
    this.username = this.authService.decodedToken.Name;
    this.signalrService.startConnection();
    this.signalrService.broadcastuserschat()
    this.signalrService.userJoined();
  this.signalrService.userLeaved();
  }

  getMessageUserList(userId: number) {
    this.messageService.getMessageUserList(userId).subscribe(result => { this.users = result }, err => { this.alertify.error(err) });
  }
  // SignalR kullanılmadan geçmiş mesajlaşmaları getiren fonksiyon. Mesaj sayfasında kişi bilgisine tıklanıldığında bu fonksiyon çalışıyor.
  getUsersChat(friendUserId: number) {
    this.sendMessages = [];
    this.messageService.getUsersChat(this.authService.decodedToken.NameId, friendUserId).subscribe(result => { this.signalrService.messages = result }, err => { this.alertify.error(err) });
    this.recipientId = friendUserId;

  }
  //SignalR kullanılan fonksiyon. Mesajlaşma penceresinde geçmiş mesajlaşmaları getirmek için bu fonksiyon kullanılıyor
  getUsersChatRT(friendUserId: number) {
    
    this.signalrService.getUsersChatSendParams(this.authService.decodedToken.NameId, friendUserId);
    this.recipientId = friendUserId;
   

  }
  sendMessage(recipientId: number, messageText: string) {
    this.messageService.sendMessage(recipientId, this.authService.decodedToken.NameId, messageText).subscribe(result => {
      this.alertify.success("Başarılı")
    });
    this.getUsersChatRT(recipientId);
  }
  sendMessageRT(recipientId: number, messageText: string) {
    this.signalrService.sendMessageRT(recipientId, messageText);
    this.messageText = '';

  }


}
